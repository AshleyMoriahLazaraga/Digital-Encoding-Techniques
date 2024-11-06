import streamlit as st
import matplotlib.pyplot as plt


def nrz_l_encoding(binary_input):
    x_values = []
    y_values = []
    time = 0
    for bit in binary_input:
        x_values.extend([time, time + 1])
        y_values.extend([1 if bit == '1' else -1] * 2)
        time += 1
    return x_values, y_values


def nrz_i_encoding(binary_input, prev_state):
    x_values = []
    y_values = []
    time = 0
    if prev_state:
        current_level = 1
    else:
        current_level = -1

    for bit in binary_input:
        x_values.extend([time, time + 1])
        if bit == '1':
            current_level = -current_level  # Invert level on '1'
        y_values.extend([current_level, current_level])
        time += 1
    return x_values, y_values


def bipolar_ami_encoding(binary_input, initial_high):
    x_values = []
    y_values = []
    time = 0
    # last_level = 1
    if initial_high:
        last_level = 1
    else:
        last_level = -1

    for bit in binary_input:
        x_values.extend([time, time + 1])
        if bit == '1':
            last_level = -last_level
            y_values.extend([last_level, last_level])
        else:
            y_values.extend([0, 0])
        time += 1
    return x_values, y_values


def pseudoternary_encoding(binary_input, initial_high):
    x_values = []
    y_values = []
    time = 0
    if initial_high:
        last_level = 1
    else:
        last_level = -1

    for bit in binary_input:
        x_values.extend([time, time + 1])
        if bit == '0':
            last_level = -last_level
            y_values.extend([last_level, last_level])
        else:
            y_values.extend([0, 0])
        time += 1
    return x_values, y_values


def manchester_encoding(binary_input):
    x_values = []
    y_values = []
    time = 0
    for bit in binary_input:
        x_values.extend([time, time + 0.5, time + 0.5, time + 1])
        if bit == '0':  # high to low
            y_values.extend([1, 1, -1, -1])
        if bit == '1':  # low to high
            y_values.extend([-1, -1, 1, 1])
        time += 1
    return x_values, y_values


def differential_manchester_encoding(binary_input, prev_state):
    x_values = []
    y_values = []
    time = 0
    if prev_state:
        current_level = -1
    else:
        current_level = 1

    for bit in binary_input:
        x_values.extend([time, time + 0.5, time + 0.5, time + 1])

        if bit == '1':
            current_level = -current_level
            y_values.extend([current_level, current_level, -current_level, -current_level])
        else:
            y_values.extend([current_level, current_level, -current_level, -current_level])

        time += 1

    return x_values, y_values


st.title("Digital Signal Encoding Techniques Visualizer")

binary_input = st.text_input("Enter a binary sequence (up to 16 bits): ")
initial_level_input = st.selectbox(
    "Please input initial state:",
    options=["high", "low"]
)

initial_high = initial_level_input == 'high'
prev_state = initial_high

if st.button("Generate Encodings"):
    if len(binary_input) <= 16 and all(bit in '01' for bit in binary_input):
        encodings = {
            "NRZ-L": nrz_l_encoding(binary_input),
            "NRZ-I": nrz_i_encoding(binary_input, prev_state),
            "Bipolar AMI": bipolar_ami_encoding(binary_input, initial_high),
            "Pseudoternary": pseudoternary_encoding(binary_input, initial_high),
            "Manchester": manchester_encoding(binary_input),
            "Differential Manchester": differential_manchester_encoding(binary_input, prev_state)
        }

        for encoding_name, (x_values, y_values) in encodings.items():
            fig, ax = plt.subplots()
            ax.step(x_values, y_values, where='post')
            ax.set(title=encoding_name)
            ax.grid(True)
            ax.set_ylim(-2, 2)

            for i, bit in enumerate(binary_input):
                ax.text(i + 0.5, 1.5, bit, ha='center', va='center', fontsize=12, fontweight='bold')

            st.pyplot(fig)
    else:
        st.error("Invalid input. Please enter a binary sequence up to 16 bits containing only '0' and '1'.")