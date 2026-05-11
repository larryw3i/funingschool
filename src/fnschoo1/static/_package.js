import * as fs from 'fs'
import * as path from 'path'

const package_dir = import.meta.dirname
const package_path = path.join(package_dir, 'package.json')
const data = fs.readFileSync(package_path, 'utf8')
const package_info = JSON.parse(data)

const locale_dir = path.join(package_dir, 'locale')
const source_dir = path.join(package_dir, 'src')

export { package_info, locale_dir, source_dir }

// The end.
