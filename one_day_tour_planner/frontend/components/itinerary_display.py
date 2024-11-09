import streamlit as st

def itinerary_display(itinerary):
    """
    Displays the itinerary details in a user-friendly format.

    Args:
        itinerary (list): A list of dictionaries, where each dictionary contains the details of a stop in the itinerary.
                          Each dictionary should have at least 'name' and 'time' keys, and can optionally include other keys
                          like 'transport', 'travel_cost', etc.

    Example of itinerary format:
    [
        {'name': 'Eiffel Tower', 'time': '09:00', 'transport': 'public_transport', 'travel_cost': 2.5},
        {'name': 'Louvre Museum', 'time': '11:00', 'transport': 'taxi', 'travel_cost': 15.0}
    ]
    """

    # Displaying a title for the itinerary section
    st.header("Your Optimized One-Day Itinerary")

    # Check if the itinerary is empty
    if not itinerary:
        st.write("No itinerary found. Please input your preferences.")
        return

    # Loop through each stop in the itinerary and display relevant details
    for i, stop in enumerate(itinerary):
        # Display stop name and time
        st.subheader(f"Stop {i + 1}: {stop['name']}")
        st.write(f"Time: {stop['time']}")

        # Display additional details such as transport mode and travel cost if available
        if 'transport' in stop:
            st.write(f"Transport: {stop['transport']}")
        
        if 'travel_cost' in stop:
            st.write(f"Travel Cost: ${stop['travel_cost']:.2f}")

        # Add a separator between stops for better readability
        st.write("---")
    
    # Optionally, display a summary of the total cost if it is available in the itinerary
    total_cost = sum([stop.get('travel_cost', 0) for stop in itinerary])
    st.write(f"**Total Estimated Travel Cost: ${total_cost:.2f}**")
