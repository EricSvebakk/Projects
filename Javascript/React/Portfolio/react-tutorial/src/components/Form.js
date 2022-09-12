
import React, { Component } from "react";

class Form extends Component {
	
	initialState = {
		name: "",
		job: "",
	}
	
	state = this.initialState
	
	// Class method
	handleChange = (event) => {
		const {name, value} = event.target
		
		this.setState(
			{
				[name]: value,
			}
		)
	}
	
	// class method
	submitForm = () => {
		this.props.handleSubmit(this.state)
		this.setState(this.initialState)
	}
	
	render() {
		const {name, job} = this.state
		
		return (
			<form className="myFormOuter testBorder">
				<div className="myFormInner testBorder">
					<label htmlFor="name">Name</label>
					<input 
						type="text"
						name="name"
						id="name"
						value={name}
						onChange={this.handleChange}
					/>
				</div>
				<div className="myFormInner testBorder">
					<label htmlFor="job">Job</label>
					<input
						type="text"
						name="job"
						id="job"
						value={job}
						onChange={this.handleChange}
					/>
				</div>
				<div className="myFormInner testBorder">
					<input
						type="button"
						value="Submit!!"
						onClick={this.submitForm}
					/>
				</div>
			</form>
		)
	}
}

export default Form;