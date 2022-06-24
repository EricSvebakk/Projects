
import React, { Component } from 'react'
import Table from './Table'
import Form from './Form'

class App extends Component {
	
	// state allows data to be saved AND modified
	state = {
		characters: [
			{
				name: "Charlie",
				job: "janitor"
			},
			{
				name: 'Mac',
				job: 'Bouncer',
			},
			{
				name: 'Dee',
				job: 'Aspring actress',
			},
			{
				name: 'Dennis',
				job: 'Bartender',
			},
		]
	}
	
	// class method
	removeCharacter = (index) => {
		
		const {characters} = this.state

		this.setState(
			{
				characters: characters.filter(
					(character, i) => {
						return i !== index
					}
				),
			}
		)

	}
	
	// class method
	handleSubmit = (character) => {
		this.setState(
			{
				characters: [...this.state.characters, character]
			}
		)
	}
	
	render() {	
		const {characters} = this.state
		
		return (
			<div className="container">
				<h1>this is a table</h1>
				<Table
					characterData={characters}
					removeCharacter={this.removeCharacter}
				/>
				<Form
					handleSubmit={this.handleSubmit}
				/>
			</div>
		)
	}
}

export default App