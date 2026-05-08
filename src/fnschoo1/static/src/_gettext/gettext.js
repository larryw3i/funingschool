const fs = require('fs')
const path = require('path')
const { package_info, locales_dir, source_dir } = require(
  path.join(path.dirname(__dirname), '_package.js')
)
const gettextParser = require('gettext-parser')

class GettextI18n {
  constructor(options = {}) {
    this.locale = options.locale || 'en'
    this.domain = options.domain || package_info.name
    this.localeDir = options.localeDir || locales_dir
    this.catalog = null

    this.loadCatalog()
  }

  loadCatalog() {
    try {
      const moPath = path.join(
        this.localeDir,
        this.locale,
        'LC_MESSAGES',
        `${this.domain}.mo`
      )

      const poPath = path.join(
        this.localeDir,
        this.locale,
        'LC_MESSAGES',
        `${this.domain}.po`
      )

      if (fs.existsSync(moPath)) {
        const moData = fs.readFileSync(moPath)
        this.catalog = gettextParser.mo.parse(moData)
      } else if (fs.existsSync(poPath)) {
        const poData = fs.readFileSync(poPath, 'utf8')
        this.catalog = gettextParser.po.parse(poData)
      } else {
        console.warn(`No translation catalog found for locale: ${this.locale}`)
        this.catalog = { translations: {} }
      }
    } catch (error) {
      console.error('Failed to load translation catalog:', error)
      this.catalog = { translations: {} }
    }
  }

  gettext(msgid) {
    if (!this.catalog || !this.catalog.translations['']) {
      return msgid
    }

    const translation = this.catalog.translations[''][msgid]
    if (translation && translation.msgstr[0]) {
      return translation.msgstr[0]
    }

    return msgid
  }

  ngettext(msgid, msgidPlural, count) {
    if (!this.catalog || !this.catalog.translations['']) {
      return count === 1 ? msgid : msgidPlural
    }

    const translation = this.catalog.translations[''][msgid]
    if (!translation || !translation.msgstr) {
      return count === 1 ? msgid : msgidPlural
    }

    const index = count === 1 ? 0 : 1
    if (translation.msgstr[index]) {
      return translation.msgstr[index]
    }

    return count === 1 ? msgid : msgidPlural
  }

  setLocale(locale) {
    this.locale = locale
    this.loadCatalog()
  }

  getLocale() {
    return this.locale
  }
}

const sys_locale =
  process.env.LANG ||
  process.env.LANGUAGE ||
  process.env.LC_ALL ||
  process.env.LC_MESSAGES ||
  'en_US.UTF-8'

const i18n = new GettextI18n({
  locale: sys_locale.split('.')[0],
  localeDir: locales_dir,
  domain: package_info.name,
})

function _(msgid) {
  return i18n.gettext(msgid)
}

function ngettext(msgid, msgidPlural, count) {
  return i18n.ngettext(msgid, msgidPlural, count)
}

module.exports = {
  _,
  ngettext,
}

// The end.
