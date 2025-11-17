from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = 'X6bcYYVWiKi2VhDRFij4dErDszBeJVsWRe0YFvG9'

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/search', methods=['POST'])
def search():
    receta_name = request.form.get('name', '').strip().lower()
    if not receta_name:
        flash('Por favor ingresa un nombre de receta válida.', 'error')
        return redirect(url_for('base'))

    try:
        api_key = 'X6bcYYVWiKi2VhDRFij4dErDszBeJVsWRe0YFvG9'
        url = f'https://api.nal.usda.gov/fdc/v1/foods/search?query={receta_name}&api_key={api_key}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            if not data.get('foods'):
                flash(f'Receta "{receta_name}" no encontrada.', 'error')
                return redirect(url_for('base'))

            receta = data['foods'][0]

            receta_info = {
                'name': receta.get('description', 'Desconocida'),
                'brand': receta.get('brandOwner', 'Desconocida'),
                'calorias': next((n['value'] for n in receta.get('foodNutrients', []) if n['nutrientName'] == 'Energy'), 'N/A'),
                'proteina': next((n['value'] for n in receta.get('foodNutrients', []) if n['nutrientName'] == 'Protein'), 'N/A'),
                'grasa': next((n['value'] for n in receta.get('foodNutrients', []) if n['nutrientName'] == 'Total lipid (fat)'), 'N/A'),
                'carbohidratos': next((n['value'] for n in receta.get('foodNutrients', []) if n['nutrientName'] == 'Carbohydrate, by difference'), 'N/A')
            }

            return render_template('nutri.html', receta=receta_info)

        else:
            flash('Error al conectar con la API de recetas. Inténtalo más tarde.', 'error')
            return redirect(url_for('base'))

    except requests.exceptions.RequestException:
        flash('Error al conectar con la API de recetas. Inténtalo de nuevo más tarde.', 'error')
        return redirect(url_for('base'))


if __name__ == '__main__':
    app.run(debug=True)
