import streamlit as st
import numpy as np

# Set the background image and color
st.set_page_config(page_title="SLE CALC", layout="wide", page_icon=":skull:")

st.markdown("""
        <h1 style="font-size: 100px; font-family: 'Courier' ; text-align: center; color: green">
        SLE CALC 
        </h1>
    """, unsafe_allow_html=True)

# Get the size of the matrices from the user
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
            <h1 style="font-size: 30px; font-family: 'Courier'; text-align: left; color: green">
            INPUT NUMBER OF EQUATIONS   >>>
            </h1>
        """, unsafe_allow_html=True)
with col2:
    num_equations = st.number_input("", min_value=2, max_value=5, key='num_equations')

# Create empty lists to store the coefficients and constants
coefficients = []
constants = []

# Get the coefficients and constants from the user
col1, col2 = st.columns([1,2])
with col1:
    st.markdown("""
            <h1 style="font-size: 20px; font-family: 'Courier'; text-align: left; color: green">
            Input for the Coefficients and Constants >>>
            </h1>
        """, unsafe_allow_html=True)
with col2:
    for i in range(num_equations):
        st.markdown(f"""
                    <h1 style="font-size: 30px; font-family: 'Courier'; text-align: left; color: green">
                    Equation {i + 1}
                    </h1>
                """, unsafe_allow_html=True)
        st.subheader("")
        col = st.columns(num_equations, gap="medium")
        row_coeffs = []
        for j in range(num_equations):
            with col[j]:
                st.markdown(f"""
                            <h1 style="font-size: 30px; font-family: 'Courier'; text-align: left; color: green">
                            {chr(65 + j)}
                            </h1>
                        """, unsafe_allow_html=True)
                coeff = st.number_input("", key=f"coeff_{i}_{j}", format="%f")
                row_coeffs.append(coeff)
        st.markdown("""
                                    <h1 style="font-size: 30px; font-family: 'Courier'; text-align: left; color: green">
                                    Constant
                                    </h1>
                                """, unsafe_allow_html=True)
        constants.append(st.number_input("", key=f"const_{i}"))
        coefficients.append(row_coeffs)

# Create the coefficient and constant matrices
coefficient_matrix = np.array(coefficients)
constant_matrix = np.array(constants)

# Define a function to perform Gaussian elimination
def gaussian_elimination(A, B):
    n = len(A)
    for i in range(n):
        # Search for maximum in this column
        max_el = abs(A[i][i])
        max_row = i
        for k in range(i + 1, n):
            if abs(A[k][i]) > max_el:
                max_el = abs(A[k][i])
                max_row = k
        # Swap maximum row with current row (column by column)
        for k in range(i, n):
            tmp = A[max_row][k]
            A[max_row][k] = A[i][k]
            A[i][k] = tmp
        tmp = B[max_row]
        B[max_row] = B[i]
        B[i] = tmp
        # Make all rows below this one 0 in current column
        for k in range(i + 1, n):
            c = -A[k][i] / A[i][i]
            for j in range(i, n):
                if i == j:
                    A[k][j] = 0
                else:
                    A[k][j] += c * A[i][j]
            B[k] += c * B[i]
    return A, B

# Define a function to solve the system of equations using Gaussian elimination
def solve_system_gaussian_elimination(coefficient_matrix, constant_matrix):
    A, B = gaussian_elimination(np.copy(coefficient_matrix), np.copy(constant_matrix))
    n = len(A)
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = B[i] / A[i][i]
        for k in range(i - 1, -1, -1):
            B[k] -= A[k][i] * x[i]
    return x, A, B

# Add a button to solve the system of equations
if st.button("Calculate"):
    # Check if the coefficient matrix is square
    if coefficient_matrix.shape[0] != coefficient_matrix.shape[1]:
        st.error("The coefficient matrix must be square.")
    else:
        # Check if the determinant of the coefficient matrix is non-zero
        if np.linalg.det(coefficient_matrix) == 0:
            st.error("Please input valid Coefficients and Constants.")
        else:
            # Solve the system of equations using Gaussian elimination
            solution, A, B = solve_system_gaussian_elimination(coefficient_matrix, constant_matrix)
            # Display the step-by-step solution
            st.markdown("""
                                <h1 style="font-size: 20px; font-family: 'Courier'; text-align: left; color: green">
                                Step-by-Step Solution using Gaussian Elimination:
                                </h1>
                            """, unsafe_allow_html=True)
            st.subheader("Upper Triangular Form of Coefficient Matrix (After Gaussian Elimination):")
            st.write(np.round(A, 2))
            st.subheader("Transformed Constants:")
            st.write(np.round(B, 2))
            st.subheader("Solution:")
            for i, root in enumerate(solution):
                st.write(f"{chr(65 + i)}: {root}")

# Add divider
st.divider()

# Add credits
col1, col2, col3, col4, col5 = st.columns(5)
with col3:
    st.markdown("""
                                    <h1 style="font-size: 50px; font-family: 'Courier'; text-align: left; color: green">
                                    SAM x JOHN
                                    </h1>
                                """, unsafe_allow_html=True)
with col4:
    st.image("https://scontent.fceb1-5.fna.fbcdn.net/v/t1.18169-9/12108953_1012035392190327_160100101674232912_n.jpg?_nc_cat=110&ccb=1-7&_nc_sid=5f2048&_nc_eui2=AeGrZJ9AqbfKMd1w2ekFf8gIF8f6N_MyByYXx_o38zIHJg5abDwz9I6VCXSVGgQ1aMNuRDroxy3b7XYJD-Kjoo8I&_nc_ohc=Bf92Bt4uGq0Q7kNvgG1uCTm&_nc_ht=scontent.fceb1-5.fna&oh=00_AYBu_I--qUnHZmaQ5YWRABpFekPsWNxV_3PgkYFICLHyXw&oe=6668FFD4", width=300)
with col5:
    st.image("https://scontent.fceb1-2.fna.fbcdn.net/v/t1.6435-9/54517485_2241116456217301_2417532907896700928_n.jpg?_nc_cat=111&ccb=1-7&_nc_sid=5f2048&_nc_eui2=AeGVu-AKlQsfzKN52qsFpBEDNguGFrk6TJw2C4YWuTpMnKk7nWD3u6TRI3lLTmxoeNRxGF9L50yas_vzwE8Hcs2T&_nc_ohc=ZuTd6Qf3EYQQ7kNvgE5-K_B&_nc_ht=scontent.fceb1-2.fna&oh=00_AYAVnXRyIBmVE3AFQ85VW46yp9XuC9fqLOk-SGAn_Bv2cA&oe=66690878", width=300)
