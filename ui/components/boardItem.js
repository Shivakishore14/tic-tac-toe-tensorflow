import React from 'react';
import ReactDOM from 'react-dom';
export default class BoardItem extends React.Component {
	constructor(){
		super();
    }
	render(){
        const itemStyle = {
            height : "30px",
            border : "1px solid black",
            margin : "1px"
        }
        const imgStyle = {
            height : "20px"
        }
        let image = "/assets/none.jpeg";
        if(this.props.currentItem == "x"){
            image = "/assets/x.png";
        }else if(this.props.currentItem == "o"){
            image = "/assets/o.png";
        }
        return (
            <div style={itemStyle} onClick={() => this.props.updateItem(this.props.number)}>
                <img src={image} style={imgStyle}/>
            </div>
        );
	}
}
