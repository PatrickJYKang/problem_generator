import requests
import json
import os
import time
import tempfile

class GitHubFetcher:
    """Utility class for fetching content from GitHub repositories"""
    
    def __init__(self, owner="ronreiter", repo="interactive-tutorials", branch="master"):
        self.owner = owner
        self.repo = repo
        self.branch = branch
        self.api_base_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
        self.raw_base_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}"
        self.cache_dir = os.path.join(tempfile.gettempdir(), f"{owner}_{repo}_{branch}")
        self.cache_expiry = 3600  # Cache expiry in seconds (1 hour)
        
        # Create cache directory if it doesn't exist
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Define custom course structures for sites without index.json
        self.custom_structures = {
            "learn-cpp.org": {
                "basics": {
                    "Hello, World!": "Hello, World!",
                    "Variables and Types": "Variables and Types",
                    "Arrays": "Arrays",
                    "Strings": "Strings",
                    "if-else": "if-else",
                    "For loops": "For loops",
                    "While loops": "While loops",
                    "Functions": "Functions"
                },
                "advanced": {
                    "Pointers": "Pointers",
                    "Structures": "Structures",
                    "Function arguments by reference": "Function arguments by reference",
                    "Dynamic allocation": "Dynamic allocation",
                    "Recursion": "Recursion",
                    "Linked lists": "Linked lists",
                    "Binary trees": "Binary trees",
                    "Function Pointers": "Function Pointers",
                    "Template Metaprogramming": "Template Metaprogramming"
                }
            }
        }
    
    def _get_cache_path(self, path):
        """Convert a repo path to a cache file path"""
        # Replace slashes and other problematic characters
        safe_path = path.replace('/', '_').replace('\\', '_')
        return os.path.join(self.cache_dir, safe_path)
    
    def _is_cache_valid(self, cache_path):
        """Check if a cached file is still valid"""
        if not os.path.exists(cache_path):
            return False
        
        # Check if the file is older than the cache expiry time
        mtime = os.path.getmtime(cache_path)
        return (time.time() - mtime) < self.cache_expiry
    
    def get_file_content(self, path, use_cache=True):
        """
        Get the content of a file from the GitHub repository
        
        Args:
            path: Path to the file in the repository
            use_cache: Whether to use cached content if available
            
        Returns:
            The content of the file as a string
        """
        print(f"Fetching file content for path: {path}")
        cache_path = self._get_cache_path(path)
        
        # Check if we have a valid cached version
        if use_cache and self._is_cache_valid(cache_path):
            print(f"Using cached content for {path}")
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                print(f"Error reading from cache: {str(e)}")
                # Continue to fetch from GitHub if cache read fails
        
        # Fetch from GitHub
        url = f"{self.raw_base_url}/{path}"
        print(f"Fetching from GitHub URL: {url}")
        
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                print(f"GitHub API error: Status {response.status_code}, Response: {response.text}")
                raise Exception(f"Failed to fetch file from GitHub: {url}, Status: {response.status_code}")
            
            content = response.text
            
            # Save to cache
            try:
                with open(cache_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Cached content for {path}")
            except Exception as e:
                print(f"Error writing to cache: {str(e)}")
                # Continue even if cache write fails
            
            return content
        
        except requests.RequestException as e:
            print(f"Request exception when fetching {url}: {str(e)}")
            raise Exception(f"Network error when fetching from GitHub: {str(e)}")
    
    def list_directory(self, path):
        """
        List the contents of a directory in the GitHub repository
        
        Args:
            path: Path to the directory in the repository
            
        Returns:
            A list of items in the directory
        """
        print(f"Listing directory: {path}")
        url = f"{self.api_base_url}/{path}"
        print(f"GitHub API URL: {url}")
        
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                print(f"GitHub API error: Status {response.status_code}, Response: {response.text}")
                raise Exception(f"Failed to list directory: {url}, Status: {response.status_code}")
            
            data = response.json()
            print(f"Successfully listed directory with {len(data)} items")
            return data
            
        except requests.RequestException as e:
            print(f"Request exception when listing directory {path}: {str(e)}")
            raise Exception(f"Network error when listing directory from GitHub: {str(e)}")
        except ValueError as e:
            print(f"JSON parsing error when listing directory {path}: {str(e)}")
            raise Exception(f"Failed to parse GitHub response as JSON: {str(e)}")
    
    def get_json_content(self, path, use_cache=True):
        """
        Get JSON content from a file in the GitHub repository
        
        Args:
            path: Path to the JSON file in the repository
            use_cache: Whether to use cached content if available
            
        Returns:
            The parsed JSON content
        """
        content = self.get_file_content(path, use_cache)
        return json.loads(content)
    
    def get_lessons(self, language="learnpython.org", lang="en"):
        """
        Get lessons for a specific language tutorial
        
        Args:
            language: The tutorial language (e.g., learnpython.org)
            lang: The language code (e.g., en)
            
        Returns:
            The parsed index.json content for the language
        """
        print(f"Getting lessons for {language}/{lang}")
        
        # Check if we have a custom structure for this language
        if language in self.custom_structures:
            print(f"Using custom structure for {language}")
            return self.custom_structures[language]
        
        # For learnpython.org, we need to ensure proper order
        if language == "learnpython.org":
            # Define the correct order for Python lessons
            # This ensures consistency regardless of JSON ordering
            python_order = {
                "basics": [
                    "Hello, World!",
                    "Variables and Types",
                    "Lists",
                    "Basic Operators",
                    "String Formatting",
                    "Basic String Operations",
                    "Conditions",
                    "Loops",
                    "Functions",
                    "Classes and Objects",
                    "Dictionaries",
                    "Modules and Packages"
                ],
                "advanced": [
                    "Generators",
                    "List Comprehensions",
                    "Multiple Function Arguments",
                    "Regular Expressions",
                    "Exception Handling",
                    "Sets",
                    "Serialization",
                    "Partial functions",
                    "Closures",
                    "Decorators",
                    "Map, Filter, Reduce",
                    "Code Introspection",
                    "Input and Output",
                    "Parsing CSV Files"
                ]
            }
            
            try:
                # Get the actual content from GitHub
                path = f"tutorials/{language}/{lang}/index.json"
                result = self.get_json_content(path)
                print(f"Successfully retrieved lessons from {path}")
                
                # Create ordered dictionary based on our predefined order
                ordered_result = {}
                
                for category in ["basics", "advanced"]:
                    if category in result:
                        ordered_result[category] = {}
                        
                        # Add lessons in the correct order, but only if they exist in the API response
                        for lesson in python_order[category]:
                            if lesson in result[category]:
                                ordered_result[category][lesson] = result[category][lesson]
                        
                        # Add any remaining lessons not in our predefined order
                        for lesson in result[category]:
                            if lesson not in ordered_result[category]:
                                ordered_result[category][lesson] = result[category][lesson]
                
                print(f"Returning ordered lessons for {language}")
                return ordered_result
                
            except Exception as e:
                print(f"Error getting ordered lessons: {str(e)}")
                # Fall through to the general case
        
        # Otherwise try to fetch from GitHub
        path = f"tutorials/{language}/{lang}/index.json"
        
        try:
            result = self.get_json_content(path)
            print(f"Successfully retrieved lessons from {path}")
            return result
        except Exception as e:
            print(f"Error getting lessons from {path}: {str(e)}")
            
            # Fallback to a simplified structure if we can't get the real lessons
            print("Providing fallback lesson structure")
            return {
                "basics": {
                    "Hello, World!": "Hello, World!",
                    "Variables and Types": "Variables and Types",
                    "Lists": "Lists",
                    "Basic Operators": "Basic Operators",
                    "String Formatting": "String Formatting",
                    "Basic String Operations": "Basic String Operations",
                    "Conditions": "Conditions",
                    "Loops": "Loops",
                    "Functions": "Functions",
                    "Classes and Objects": "Classes and Objects"
                },
                "advanced": {
                    "Generators": "Generators",
                    "List Comprehensions": "List Comprehensions",
                    "Multiple Function Arguments": "Multiple Function Arguments",
                    "Regular Expressions": "Regular Expressions",
                    "Exception Handling": "Exception Handling",
                    "Sets": "Sets",
                    "Serialization": "Serialization",
                    "Partial functions": "Partial functions",
                    "Code Introspection": "Code Introspection",
                    "Decorators": "Decorators"
                }
            }
    
    def build_syllabus(self, lesson, language="learnpython.org", lang="en"):
        """
        Build a syllabus from markdown files up to and including the current lesson
        
        Args:
            lesson: The current lesson name
            language: The tutorial language (e.g., learnpython.org)
            lang: The language code (e.g., en)
            
        Returns:
            Path to a temporary file containing the concatenated markdown
        """
        print(f"Building syllabus for {lesson} in {language}/{lang}")
        
        # Get all lessons in proper order
        all_lessons = []
        lesson_data = None
        
        # Check if we have a custom structure for this language
        if language in self.custom_structures:
            print(f"Using custom lesson order for {language}")
            lesson_data = self.custom_structures[language]
            
            # Build ordered list of lessons from the custom structure
            for category in ["basics", "advanced"]:
                if category in lesson_data:
                    all_lessons.extend(list(lesson_data[category].keys()))
        else:
            # Try to load from index.json
            try:
                index_path = f"tutorials/{language}/{lang}/index.json"
                lesson_data = self.get_json_content(index_path)
                print(f"Successfully loaded index.json for {language}")
                
                # Build ordered list of lessons from index.json
                for category in ["basics", "advanced"]:
                    if category in lesson_data:
                        all_lessons.extend(list(lesson_data[category].keys()))
            except Exception as e:
                print(f"Failed to load index.json: {str(e)}")
                return None
        
        print(f"Lesson order: {all_lessons}")
        
        # Find the position of the current lesson
        try:
            lesson_index = all_lessons.index(lesson)
            print(f"Found lesson '{lesson}' at position {lesson_index}")
        except ValueError:
            print(f"Lesson '{lesson}' not found in lesson list")
            return None
        
        # Get all lessons up to and including the current lesson
        lessons_to_include = all_lessons[:lesson_index + 1]
        print(f"Including {len(lessons_to_include)} lessons in the syllabus")
        
        # Create a temporary file to store the concatenated markdown
        temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.md')
        
        try:
            # Add a welcome message at the beginning if it exists
            try:
                welcome_content = self.get_file_content(f"tutorials/{language}/{lang}/Welcome.md")
                temp_file.write(welcome_content + "\n\n")
                print("Added Welcome.md to syllabus")
            except Exception:
                # It's okay if Welcome.md doesn't exist
                print("No Welcome.md found, skipping")
                pass
            
            # Concatenate all markdown files in order
            for lesson_name in lessons_to_include:
                try:
                    md_content = self.get_file_content(f"tutorials/{language}/{lang}/{lesson_name}.md")
                    temp_file.write(f"# {lesson_name}\n\n")
                    temp_file.write(md_content + "\n\n")
                    print(f"Added lesson: {lesson_name}")
                except Exception as e:
                    print(f"Markdown file for lesson '{lesson_name}' not found: {str(e)}")
                    
                    # For custom courses like learn-cpp.org, create placeholder content
                    if language in self.custom_structures:
                        print(f"Creating placeholder content for {lesson_name}")
                        temp_file.write(f"# {lesson_name}\n\n")
                        temp_file.write(f"This is a placeholder for the {lesson_name} lesson.\n\n")
                        temp_file.write(f"Please complete the coding challenge for {lesson_name}.\n\n")
            
            temp_file.close()
            print(f"Successfully built syllabus at {temp_file.name}")
            return temp_file.name
        except Exception as e:
            print(f"Failed to build syllabus: {str(e)}")
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)
            return None
