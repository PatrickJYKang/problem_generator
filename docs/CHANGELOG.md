# Changelog

All notable changes to the Problem Generator will be documented in this file.

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
