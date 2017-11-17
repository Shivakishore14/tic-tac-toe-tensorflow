import React from 'react';
import ReactDOM from 'react-dom';
import GameBoard from './components/gameboard'
export default class MyApp extends React.Component {
	constructor(){
		super();
	}
	render(){
		return (
		        <GameBoard />
		);
	}
}

ReactDOM.render(<MyApp/>, document.getElementById('app'));
