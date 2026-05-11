import * as fs from 'fs'
import * as path from 'path'
import { package_info, locale_dir, source_dir } from '#root/_package.js'
import { exec } from 'child_process'

var maintainer_email = 'larryw3i@yeah.net'
var langs = ['en_US', 'zh_CN']
var po_file_paths = langs.map(
  (lang) => `${locale_dir}/${lang}/LC_MESSAGES/${package_info.name}.po`
)
var pot_file_path = path.join(locale_dir, `${package_info.name}.pot`)

for (var po_file_path of po_file_paths) {
  po_file_path = path.parse(po_file_path)
  if (!fs.existsSync(po_file_path.dir)) {
    fs.mkdirSync(po_file_path.dir, { recursive: true })
  }
}

if (!fs.existsSync(locale_dir)) {
  fs.mkdirSync(locale_dir, { recursive: true })
}

function get_js_files(dirPath) {
  var files = []

  function walk(dir) {
    var items = fs.readdirSync(dir, { withFileTypes: true })

    for (var item of items) {
      var fullPath = path.join(dir, item.name)

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
  var js_files = get_js_files((dir = source_dir)).join(' ')
  var command = `\
    xgettext \
      --output="${pot_file_path}" \
      --language=JavaScript \
      --keyword=gettext:1 \
      --keyword=ngettext:1,2 \
      --from-code=UTF-8 \
      --add-comments=TRANSLATORS: \
      --package-name="${package_info.name}" \
      --package-version="1.0.0" \
      --msgid-bugs-address="${maintainer_email}" \
      ${js_files} \
    `

  exec(command, (error, stdout, stderr) => {
    if (error) {
      console.error('Error extracting strings:', error)
      return
    }
    console.log('Strings extracted to:', pot_file_path)
  })
  for (var po_file_path of po_file_paths) {
    po_file_path = path.parse(po_file_path)
    var lang_split = po_file_path.dir.split(path.sep)
    var lang = lang_split[lang_split.length - 2]
    var command = ''
    po_file_path = path.format(po_file_path)
    if (!fs.existsSync(po_file_path)) {
      command = `\
        msginit \
          --no-translator \
          --locale=${lang} \
          --input=${pot_file_path} \
          --output=${po_file_path} \
      `
    } else {
      command = `\
      msgmerge \
        --update ${po_file_path} \
        ${pot_file_path} \
      `
    }
    exec(command, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error updating ${pot_file_path}:`, error)
        return
      }
      console.log(`Updated "${pot_file_path}" from "${pot_file_path}"`)
    })
  }
}

extractStrings()

// The end.
