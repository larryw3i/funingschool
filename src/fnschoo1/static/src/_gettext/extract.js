const fs = require('fs')
const path = require('path')
const { package_info, locales_dir, source_dir } = require(
  path.join(path.dirname(path.dirname(__dirname)), '_package.js')
)
const { exec } = require('child_process')

if (!fs.existsSync(locales_dir)) {
  fs.mkdirSync(locales_dir, { recursive: true })
}

function get_js_files(dirPath) {
  const files = []

  function walk(dir) {
    const items = fs.readdirSync(dir, { withFileTypes: true })

    for (const item of items) {
      const fullPath = path.join(dir, item.name)

      if (item.isDirectory()) {
        walk(fullPath)
      } else if (
        item.isFile() &&
        item.name.endsWith('.js') &&
        !item.name.endsWith('.min.js')
      ) {
        files.push(fullPath)
      }
    }
  }

  walk(dirPath)
  return files
}

function extractStrings() {
  const potFile = path.join(locales_dir, `${package_info.name}.pot`)
  const js_files = get_js_files((dir = source_dir)).join(' ')
  const command = `xgettext \
    --output="${potFile}" \
    --language=JavaScript \
    --keyword=gettext:1 \
    --keyword=ngettext:1,2 \
    --from-code=UTF-8 \
    --add-comments=TRANSLATORS: \
    --package-name="${package_info.name}" \
    --package-version="1.0.0" \
    --msgid-bugs-address="larryw3i@yeah.net" \
    ${js_files}`

  exec(command, (error, stdout, stderr) => {
    if (error) {
      console.error('Error extracting strings:', error)
      return
    }
    console.log('Strings extracted to:', potFile)
  })
}

extractStrings()

// The end.
