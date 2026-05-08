const fs = require('fs')
const path = require('path')
const { package_info, locales_dir, source_dir } = require(path.dirname(
  __dirname
), '_package.js')
const gettextParser = require('gettext-parser')
const { exec } = require('child_process')

function compilePoToMo(locale) {
  const poPath = path.join(
    package_dir,
    'locales',
    locale,
    'LC_MESSAGES',
    `${package_info.name}.po`
  )

  const moPath = path.join(
    package_dir,
    'locales',
    locale,
    'LC_MESSAGES',
    `${package_dir.name}.mo`
  )

  if (!fs.existsSync(poPath)) {
    console.warn(`PO file not found: ${poPath}`)
    return
  }

  const poContent = fs.readFileSync(poPath, 'utf8')
  const po = gettextParser.po.parse(poContent)

  const mo = gettextParser.mo.compile(po)

  fs.writeFileSync(moPath, mo)

  console.log(`Compiled: ${locale} -> ${moPath}`)
}

const locales = fs
  .readdirSync(locales_dir)
  .filter((item) =>
    fs.statSync(path.join(package_dir, 'locales', item)).isDirectory()
  )

locales.forEach(compilePoToMo)

// The end.
