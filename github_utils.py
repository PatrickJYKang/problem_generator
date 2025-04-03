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
        # Path to the index.json file
        index_path = f"tutorials/{language}/{lang}/index.json"
        
        # Load the index.json file
        try:
            index = self.get_json_content(index_path)
        except Exception as e:
            print(f"Failed to load index.json: {str(e)}")
            return None
        
        # Find all lessons in order (combine basics and advanced)
        all_lessons = []
        for category in ["basics", "advanced"]:
            if category in index:
                all_lessons.extend(list(index[category].keys()))
        
        # Find the position of the current lesson
        try:
            lesson_index = all_lessons.index(lesson)
        except ValueError:
            print(f"Lesson '{lesson}' not found in index.json")
            return None
        
        # Get all lessons up to and including the current lesson
        lessons_to_include = all_lessons[:lesson_index + 1]
        
        # Create a temporary file to store the concatenated markdown
        temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.md')
        
        try:
            # Add a welcome message at the beginning if it exists
            try:
                welcome_content = self.get_file_content(f"tutorials/{language}/{lang}/Welcome.md")
                temp_file.write(welcome_content + "\n\n")
            except Exception:
                # It's okay if Welcome.md doesn't exist
                pass
            
            # Concatenate all markdown files in order
            for lesson_name in lessons_to_include:
                try:
                    md_content = self.get_file_content(f"tutorials/{language}/{lang}/{lesson_name}.md")
                    temp_file.write(f"# {lesson_name}\n\n")
                    temp_file.write(md_content + "\n\n")
                except Exception:
                    print(f"Markdown file for lesson '{lesson_name}' not found")
            
            temp_file.close()
            return temp_file.name
        except Exception as e:
            print(f"Failed to build syllabus: {str(e)}")
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)
            return None
