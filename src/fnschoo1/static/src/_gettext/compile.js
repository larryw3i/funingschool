const fs = require('fs')
const path = require('path')
const { package_info, locale_dir, source_dir } = require(
  path.join(path.dirname(path.dirname(__dirname)), '_package.js')
)
const { exec } = require('child_process')

const entries = fs.readdirSync(locale_dir, { withFileTypes: true });
const package_langs = entries
    .filter(d => d.isDirectory())
    .map(d => d.name);

package_langs.forEach((lang) => {
  const po_path = path.join(
        locale_dir,
        lang,
        'LC_MESSAGES',
        `${package_info.name}.po`
      )
  if (fs.existsSync(po_path)) {
    const mo_path = path.join(
          locale_dir,
          lang,
          'LC_MESSAGES',
          `${package_info.name}.mo`
        )

    const command = `\
      msgfmt -vv -o ${mo_path} ${po_path}
    `
    exec(command, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error generating "${mo_path}" from "${po_path}"`)
        return
      }
      console.log(`Generating ${mo_path} from "${po_path}" .`)
    })

  }
});

// The end.
