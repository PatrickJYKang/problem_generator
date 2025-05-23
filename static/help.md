## Basic Workflow
1. Select a course and lesson
2. Click "Generate Problem"
3. Write your solution in the code editor
4. Test with "Run Code"
5. Verify with "Check Answer"
6. Check code style with "Check Style"

## Key Features

**Header Controls**
- 📋 **History**: View past problems
- 💬 **Assistant**: AI help with coding
- ❓ **Help**: Show this guide
- 🌙/☀️ **Theme**: Toggle dark/light mode

**Code Environment**
- **Language Selector**: Switch between Python, Java, C++
- **Run**: Execute your code
- **Input**: Input data for your program
- **Console**: View output and errors
- **Reset**: Clear the console to input again

## Common Issues

**Java Code**
- Remember to keep the `public class Main` declaration (you do not have to name the class `Main`).
- Don't include package declarations

**C++ Code**
- Include necessary headers (e.g., `#include <iostream>`)
- Use `std::cin` and `std::cout` for input/output

**EOF Errors or Unexpected Outputs**

- Make sure to add inputs in the input field in the bottom right before you run your code
- Python will return an `EOF Error`, Java will return a `java.util.NoSuchElementException` (if using the Scanner class), and C++ may return unexpected outputs

**Test Cases**
- Ensure your output exactly matches the expected format
- Check for trailing or leading spaces or newlines
- Check that you are outputting the correct number of decimal places
- Check your input format

**Error Messages**
- Timeout: Your code took too long to execute
- Compilation error: Syntax issues in your code

**Style Errors**
- Style errors are detected by a linter, which follows precise rules for each language
- Style errors are not critical for code execution, but they can help you write better code
- The Format Code button in C++ automatically formats your code to follow the style rules with `clang-format`
    - A known issue is that `clang-format` formats your code with two spaces for indentation. We are working on a fix.
    - In any case, the code that `clang-format` formats is not saved, and your code reverts to the original code after you return to the problem page. We are also working on a fix for this.

All code runs securely in your browser. **Your work and Assistant chats are not automatically saved**.

## About Problem Generator

**Version**: indev 0.2 (April 2025)

Problem Generator is an educational tool designed to help you practice programming in multiple languages with dynamically generated problems, style checking, and automated feedback.

### Contact

If you have any questions or issues, please email [patrick.jy.kang@gmail.com](mailto:patrick.jy.kang@gmail.com) or raise an issue on [GitHub](https://github.com/PatrickJYKang/problem_generator/issues). For issues with specific problems, because all problems are AI generated and the prompts and such used to generate them are still at a very early stage in development, please do not expect them to be perfect. If specific problems do have issues, generally, please do not raise a new issue on GitHub, but if repeated issues with similar requests persist, please do raise an issue or email me.