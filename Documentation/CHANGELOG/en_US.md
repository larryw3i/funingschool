<hr/>

<p align="center">
    <a href="https://gitee.com/larryw3i/funingschool/blob/master/Documentation/CHANGELOG/zh_CN.md">简体中文</a> •
    <a href="https://github.com/larryw3i/funingschool/blob/master/Documentation/CHANGELOG/en_US.md">English</a>
</p>

# Changelog

## [Unreleased] - 2026-04-16

### Added

### Changed
- Generate Wrokbook File: Add `timestamp` to generated file.

### Deprecated

### Fixed

### Removed

## [20260415.80820.815] - 2026-04-15

### Added
- `Ingredient consumptions` Page: Make the Entry Fields in the table automatically scroll to the visible area when they are obscured by the header or the columns fixed on the left and one of them is inputted.

### Changed
- Start Up: When starting up on a Linux distro, there may be a situation where the browser is already open but unable to access the specified URL. Therefore, it is advisable to delay opening the browser during startup.

### Deprecated

### Fixed
- Edit Ingredient: Fixed issue the `Edit Ingredient` page be loaded with error if some `Category Name` is `None`.

### Removed

## [20260409.80155.835] - 2026-04-09

### Added

### Changed
- `Ingredients List` Page: Make total price summary more intuitive.

### Deprecated

### Fixed
- Crate New Ingredients: Update the `new_ingredients` function, prevent adding too many meal types to the database when they are `empty`.
- Ingredient Consumption: Fixed the error in displaying the ingredient progress bar on the ingredient consumption page.

### Removed

## [20260127.80117.831] - 2026-01-27

### Added
- Add **CHANGELOG.md**: Add i18n feature for `CHANGELOG.md`.
- Delete Ingredients: Add the function of batch deleting ingredients.

### Changed

### Deprecated
- Patch `202511012053_copy_profiles_to_fnprofile`: This patch will be deprecated after February 2026.

### Fixed

### Removed