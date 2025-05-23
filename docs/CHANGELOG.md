# Changelog

All notable changes to the Problem Generator will be documented in this file.

## [indev 0.2.2] - 2025-04-12

### Fixed

- Fixed home button and logo navigation not showing course/lesson selectors when clicked
- Improved style check display to group multiple errors at the same position together
- Fixed CSA problems being incorrectly stored with Python language in database instead of Java
- Added migration function to update existing CSA problems to use Java language

## [indev 0.2.1] - 2025-04-10

### Fixed

- Resolved issues with LaTeX rendering in the application through appropriate prompting with only the `$$%Your LaTeX here%$$` delimiter.

## [indev 0.2] - 2025-04-07

### Added

- Style checking functionality for all supported languages (Python, Java, C++)
- Added "Check Style" button for all programming languages
- Improved Java style checker with PMD integration
- Code formatting capability for Java and C++ with "Format Code" button
- Custom formatting rules to ensure consistent code style
- AP Computer Science A (CSA) course integration
- Local syllabus loading for CSA content
- Home button in header for easy navigation to lesson selection
- Clickable title/logo for navigating back to lesson selection
- In-depth documentation of Dify AI workflows

### Changed

- Style check UI now displays line-by-line error highlighting
- Improved error detection for common Java and C++ style issues
- Style check button only appears on problem pages (not on generate page)
- Streamlined style check error display with better user feedback
- Automatically set Java as default language for CSA course
- Improved header styling consistency between light and dark themes
- Enhanced content loading mechanism for different course types

### Fixed

- Fixed Java code style detection to properly identify spacing issues
- Fixed C++ code formatting with proper clang-format integration
- Resolved bug where style check would fail on empty code
- Fixed issues with problem navigation maintaining correct state

## [indev 0.1.1] - 2025-04-06

### Added

- Help button and modal with concise technical documentation
- KaTeX integration for LaTeX math formula rendering in problems and AI assistant responses
- Improved markdown rendering across the application

## [indev 0.1] - 2025-04-04

### Added

- Initial version of the Problem Generator application
- Multi-language support for Python, Java, and C++
- Problem generation with AI assistance
- Code editor with syntax highlighting using CodeMirror
- Code execution functionality for all supported languages
- Test case validation and checking
- Dark/Light mode toggle with IntelliJ IDEA themes (darcula and idea)
- Problem history tracking and management
- AI Assistant chatbot for helping with coding problems
- GitHub integration for fetching lesson content
- Responsive UI with smooth transitions

### Changed
- Updated testcase format to use structured JSON
- Improved GitHub fetcher to handle rate limiting and provide fallbacks

### Fixed
- Chat send button no longer reloads the page
- History display includes language information
- Code checking now uses language from the problem database
