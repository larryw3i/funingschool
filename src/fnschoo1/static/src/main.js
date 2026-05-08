const fs = require('fs')
const path = require('path')
const { _, ngettext } = require(path.join(__dirname, '_gettext', 'gettext.js'))
const { package_info, locales_dir, source_dir } = require(
  path.join(__dirname, '_package.js')
)

const uglify = require('uglify-js')
const chokidar = require('chokidar')

function minifyFile(filePath) {
  const dir = path.dirname(filePath)
  const ext = path.extname(filePath)
  const basename = path.basename(filePath, ext)
  const minName = `${basename}.min${ext}`
  const minPath = path.join(dir, minName)

  try {
    const code = fs.readFileSync(filePath, 'utf8')
    const result = uglify.minify(code, {
      compress: true,
      mangle: true,
      sourceMap: {
        filename: minName,
        url: $`${minName}.map`,
        includeSources: true,
      },
      output: {
        beautify: false,
        comments: false,
      },
    })

    if (result.error) {
      console.error(
        _(`An error occurred during compression "${filePath}": ${result.error}`)
      )
      return
    }

    fs.writeFileSync(minPath, result.code, 'utf8')
    console.log(_(`"${minPath}" has been generated.`))
  } catch (error) {
    console.error(
      _(`An error occurred during generating "${minPath}": ${error.message}`)
    )
  }
}

function processAllJsFiles() {
  const jsFiles = []

  function walk(dir) {
    const files = fs.readdirSync(dir)

    for (const file of files) {
      const filePath = path.join(dir, file)
      const stat = fs.statSync(filePath)

      if (stat.isDirectory()) {
        if (file !== 'node_modules') {
          walk(filePath)
        }
      } else if (file.endsWith('.js') && !file.endsWith('.min.js')) {
        jsFiles.push(filePath)
      }
    }
  }

  walk(process.cwd())

  console.log(
    jsFiles.length > 1
      ? _(`${jsFiles.length} JS Files found.`)
      : _(`One JS File found.`)
  )
  jsFiles.forEach(minifyFile)
}

function main() {
  const isWatchMode = process.argv.includes('--watch')

  if (isWatchMode) {
    console.log(_('Start monitoring changes to .js files...'))

    const watcher = chokidar.watch('**/*.js', {
      ignored: /(^|[\/\\])\../,
      persistent: true,
      ignoreInitial: true,
      ignored: ['**/node_modules/**', '**/*.min.js'],
    })

    watcher
      .on('add', (filePath) => {
        console.log(_(`New file: ${filePath}`))
        minifyFile(filePath)
      })
      .on('change', (filePath) => {
        console.log(_(`File changed: ${filePath}`))
        minifyFile(filePath)
      })
      .on('unlink', (filePath) => {
        const dir = path.dirname(filePath)
        const ext = path.extname(filePath)
        const basename = path.basename(filePath, ext)
        const minPath = path.join(dir, `${basename}.min${ext}`)

        if (fs.existsSync(minPath)) {
          fs.unlinkSync(minPath)
          console.log(_(`File removed: ${minPath}`))
        }
      })

    processAllJsFiles()
  } else {
    processAllJsFiles()
  }
}

process.on('SIGINT', () => {
  console.log(_('Exit.'))
  process.exit(0)
})

main()

// The end.
