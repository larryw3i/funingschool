const fs = require('fs')
const path = require('path')

const package_dir = __dirname
const packagePath = path.join(__dirname, 'package.json')
const data = fs.readFileSync(packagePath, 'utf8')
const package_info = JSON.parse(data)

const locale_dir = path.join(package_dir, 'locale')
const source_dir = path.join(package_dir, 'src')

module.exports = {
  package_info,
  locale_dir,
  source_dir,
}

// The end.
