
# import uuid
from django.core.management import BaseCommand
from account.helpers.reusable import generate_account_number
from collections import Counter
from waste_auth.resume_parser import parse_resume, extract_phone, extract_resume_info


def is_palindrome(s: str) -> bool:
    """
    Check if a given string is a palindrome.
    Args:
        s (str): The string to be checked.
    Returns:
        bool: True if the string is a palindrome, False otherwise.
    """
    s = s.replace(" ", "").lower() 
    return s == s[::-1]

def first_unique_char(s: str) -> str:
    """
    Find the first non-repeating character in a string.
    Args:
        s (str): The string to be checked.
    Returns:
        str: The first non-repeating character in the string.
    """
    for char in s:
        if s.count(char) == 1:
            return char
    return ""

def unique(s: str) -> str:
  for char in s:
    if s.count(char)  == 1:
      return char
  return ""

def revered_(s: str) -> bool:

  s = s.replace(" ", "").lower()
  return s == s[::-1]


def are_anagrams(s1: str, s2: str) -> bool:

  return sorted(s1) == sorted(s2)
  # return Counter(s1) == Counter(s2)

def are_anagrams_words(s1: str, s2: str) -> bool:
    if len(s1) != len(s2):  # Quick check for different lengths
        return False

    char_count = {}

    # Count occurrences in s1
    for char in s1:
        char_count[char] = char_count.get(char, 0) + 1

    # Reduce counts based on s2
    for char in s2:
        if char not in char_count or char_count[char] == 0:
            return False  # Character missing or extra in s2
        char_count[char] -= 1

    return True  # If all counts are balanced, it's an anagram

def sec_largest_num(arr: list) -> int:
    """
    Find the second largest number in a list of integers.
    Args:
        arr (list): A list of integers.
    Returns:
        int: The second largest number in the list.
    """

    if len(arr) < 2:
        return None  # Not enough elements
    first, second = float('-inf'), float('-inf')

    for num in arr:
        if num > first:
            second, first = first, num  # Update first and second
        elif first > num > second:
            second = num  # Update second if it's smaller than first but larger than current second

    return second if second != float('-inf') else None


def move_zeros(arr: list) -> None:
    """
    Moves all zeroes in the list to the end while maintaining the order of non-zero elements.
    Args:
        arr (list): The list of integers.
    Returns:
        None (Modifies the list in-place)
    """
    non_zero_index = 0  # Pointer for placing non-zero elements
    # Move all non-zero elements forward
    for i in range(len(arr)):
        if arr[i] != 0:
            arr[non_zero_index], arr[i] = arr[i], arr[non_zero_index]
            non_zero_index += 1
    return arr
              

def settle(arr: list)-> None:
  for i in range(len(arr)):
    if arr[i] == 1:
      print(i)
      arr.append(arr.pop(i))
      print(arr)

def settle_2(arr: list) -> None:
    # Pointer for the position to place the next non-1 element
    write_pointer = 0
    # First pass: Move all non-1 elements to the front
    for pointer in range(len(arr)):
        if arr[pointer] != 1:
            arr[write_pointer] = arr[pointer]
            write_pointer += 1
    # Second pass: Fill the remaining positions with 1s
    while write_pointer < len(arr):
        arr[write_pointer] = 1
        write_pointer += 1
    print(arr)

def majority_element(nums: list) -> int:
    """
    Finds the majority element in a list (the element that appears more than ⌊n/2⌋ times).
    Args:
        nums (list): The list of integers.
    Returns:
        int: The majority element.
    """
    candidate = None
    count = 0
    # Step 1: Find the candidate for majority element
    for num in nums:
        if count == 0:
            candidate = num  # Set a new candidate
        count += (1 if num == candidate else -1)
    return candidate


class Command(BaseCommand):
  help = ""
  def handle(self, *args, **options):
    # test = assign_agent_to_product()

    # print(test)

    file_path = r"/Users/segunoloyede/Downloads/OLUWASEGUN OLOYEDE - RESUME.pdf"
    candidate_information = parse_resume(file_path)
    print("This it the", candidate_information)
    print("Done")
  







