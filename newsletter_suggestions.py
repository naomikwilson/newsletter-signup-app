from newsletter_data import newsletter_data, categories_and_index


def get_newsletter_suggestions(categories):
    """
    Returns dict with suggested newsletter names and links based on categories
    """
    newsletter_names_to_sort = []
    unsorted_suggestions = {}
    sorted_suggestions = {}

    for category in categories:

        # Get dict containing all newsletters for category
        index = categories_and_index[category]
        newsletters = newsletter_data[index][category]

        for name, link in newsletters.items():
            # Get just names for sorting
            newsletter_names_to_sort.append(name)
            # Have names and corresponding links for reference after sorting names
            unsorted_suggestions[name] = link 


    # Alphabetically sort all names of suggested newsletters
    sorted_names = merge_sort(newsletter_names_to_sort)

    # Connect links to sorted names
    for name in sorted_names:  
        sorted_suggestions[name] = unsorted_suggestions[name]

    return sorted_suggestions


def merge_sort(arr):
    """
    Sort arr (list of str.) in alphabetical order using merge sort
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left, right = arr[:mid], arr[mid:]

    left = merge_sort(left)
    right = merge_sort(right)

    return merge(left, right)


def merge(left, right):
    """
    Merges two sorted lists into a single sorted list
    """
    result, left_idx, right_idx = [], 0, 0

    while left_idx < len(left) and right_idx < len(right):
        if left[left_idx] < right[right_idx]:
            result.append(left[left_idx])
            left_idx += 1
        else:
            result.append(right[right_idx])
            right_idx += 1

    result.extend(left[left_idx:])
    result.extend(right[right_idx:])

    return result


def main():
    example_newsletter_categories = ["Current Events", "Science", "Health and Medicine"]
    print(get_newsletter_suggestions(example_newsletter_categories))


if __name__ == "__main__":
    main()
