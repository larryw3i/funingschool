const fs = require('fs')
const path = require('path')
const { _ } = require(path.join(__dirname, '_gettext', 'gettext'))
const { package_info, locales_dir, source_dir } = require(
  path.join(path.dirname(__dirname), '_package')
)

// The end.
