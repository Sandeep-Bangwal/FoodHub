# categories = ['Bakery', 'food']
# category_string = ", ".join(categories)
# print(category_string)

import random
import string

def generate_random_string(length):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

random_string = generate_random_string(6)
print(random_string)


# import datetime

# # Get user input for open time
# open_time_str = input("Enter the open time (format: HH:MM AM/PM): ")

# # Convert open time to datetime object
# open_time = datetime.datetime.strptime(open_time_str, '%I:%M %p')

# # Get user input for close time
# close_time_str = input("Enter the close time (format: HH:MM AM/PM): ")

# # Convert close time to datetime object
# close_time = datetime.datetime.strptime(close_time_str, '%I:%M %p')

# # Calculate time remaining until close time
# time_remaining = close_time - datetime.datetime.now()

# # Output time remaining in hours and minutes
# print(f"Time remaining until {close_time.strftime('%I:%M %p')} is {time_remaining.days} days, {time_remaining.seconds // 3600} hours, and {(time_remaining.seconds // 60) % 60} minutes.")
        # {% with min_price=rest.menu.all|dictsort:'price'|first %}
        #                 {% if min_price %}
        #                     <p class="card-text text-muted">
        #                         Minimum Price: {{ min_price.price }}
        #                     </p>
        #                 {% else %}
        #                     <p class="card-text text-muted">No menu available</p>
        #                 {% endif %}
        #             {% endwith %}