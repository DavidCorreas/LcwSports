# Build a streamlit app to book tournament 
import json
import streamlit as st
import pandas as pd


json_file = 'reservations.json'

def main():
    # Set title
    st.title('LCW ESPORTS')

    # Create a sidebar
    with st.sidebar:
        st.image('rocket-league-consejos-debutante.png')
        st.title('Reserva tu puesto')

    # Create a calendar
    st.subheader('Selecciona una fecha')
    date_selected = st.date_input('Fecha', min_value=None, max_value=None, value=None, key=None)

    # Create a button to book a tournament
    st.subheader('Hacer Reserva')
    # Create input text
    name = st.text_input('Nombre', value='', max_chars=None, key=None, type='default')
    if st.button('Reserva'):
        # Save the date in a file
        with open(json_file, 'r') as f:
            reservations = json.load(f)
        if date_selected.strftime('%Y-%m-%d') in reservations:
            reservations[date_selected.strftime('%Y-%m-%d')].append(name)
        else:
            reservations[date_selected.strftime('%Y-%m-%d')] = [name]
        with open(json_file, 'w+') as f:
            json.dump(reservations, f)
        

    # Display reservation on selected day
    st.subheader('Reservas Activas')
    with open(json_file, 'r') as f:
        reservations = json.load(f)
    if date_selected.strftime('%Y-%m-%d') in reservations:
        reservations = {date_selected.strftime('%Y-%m-%d'): reservations[date_selected.strftime('%Y-%m-%d')]}
    
    # Show reservation in a table with columns: date, name, delete reservation
    colms = st.columns((1, 2, 1))
    fields = ["Dia", 'Nombre', "Borrar Reserva"]
    for i, field in enumerate(fields):
        colms[i].text(field)


    # For every day in the json file, show the reservations
    for date, names in reservations.items():
        # If the date is selected, show the reservations
        for name in names:
            row_plh = st.empty()
            colms = row_plh.columns((1, 2, 1))
            colms[0].text(date)
            colms[1].text(name)
            if colms[2].button('Borrar Reserva', key=f'{date}-{name}'):
                with open(json_file, 'r') as f:
                    reservations = json.load(f)
                reservations[date].remove(name)
                if len(reservations[date]) == 0:
                    del reservations[date]
                with open(json_file, 'w+') as f:
                    json.dump(reservations, f)
                row_plh.empty()

# Start the app
if __name__ == '__main__':
    # Create json file if it doesn't exist
    try:
        with open(json_file, 'r') as f:
            pass
    except FileNotFoundError:
        with open(json_file, 'w') as f:
            json.dump({}, f)
    main()
