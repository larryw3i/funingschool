const fs = require('fs')
const path = require('path')
const { package_info, locale_dir, source_dir } = require(
  path.join(path.dirname(path.dirname(__dirname)), '_package')
)
const Gettext = require('node-gettext');
const { mo } = require( 'gettext-parser')
const { sprintf } = require('sprintf-js');


const gettext = new Gettext();

function get_sys_lang() {
  const sys_locale =
    process.env.LANG ||
    process.env.LANGUAGE ||
    process.env.LC_ALL ||
    process.env.LC_MESSAGES ||
    'en_US.UTF-8'
  return sys_locale.split('.')[0]
}
const sys_lang=get_sys_lang()
const entries = fs.readdirSync(locale_dir, { withFileTypes: true });
const package_langs = entries
    .filter(dirent => dirent.isDirectory())
    .map(dirent => dirent.name);
package_langs.forEach((lang)=>{
  const mo_path = path.join(
        locale_dir,
        lang,
        'LC_MESSAGES',
        `${package_info.name}.mo`
      )
  if (fs.existsSync(mo_path)) {
    console.log(lang,mo_path)
    const mo_data = fs.readFileSync(mo_path);

    gettext.addTranslations(lang, package_info.name, mo.parse(mo_data));
  }
});
gettext.setLocale(get_sys_lang());
gettext.textdomain(package_info.name);

function _(...args) {
    const msg_id = args[0];
    const translatedString = gettext.gettext(msg_id);
    console.log(args,msg_id,translatedString)
    return sprintf(translatedString, ...args.slice(1));
}

module.exports = {
  _
}

// The end.
