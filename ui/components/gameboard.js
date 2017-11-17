import React from 'react';
import ReactDOM from 'react-dom';
import BoardItem from './boardItem';
import Service from './services';
import axios from 'axios';

const BASE_URL = "http://localhost:5000";
const FINISHED = 0;
const RUNNING = 1;
const TIE = 2;
export default class GameBoard extends React.Component {
	constructor(){
		super();
        let initState = ["", "", "", "", "", "", "", "", ""];
        this.state = {gameboard: initState, next: "x", isFinished:false, history:[], gameStatus : RUNNING, debug:{} }
        this.updateItem = this.updateItem.bind(this);
        this.saveTrainingData = this.saveTrainingData.bind(this);
        this.predict = this.predict.bind(this);
    }
    updateItem(number){
        let flagChanged = false;
        let newGameBoardState = this.state.gameboard.map ( (elt, i) =>{
                if (number === i && elt === "") {
                    flagChanged = true;
                    return this.state.next;
                } else {
                    return elt;
                }
            }
        )
        if(flagChanged === true && this.state.isFinished == false){
                let newItem = "x";
                let msg = "";
                let finishedFlag = false;
                let current = {state:this.state.gameboard, move:number, player:this.state.next}
                let history = [...this.state.history, current]
                if (this.state.next == "x")
                    newItem = "o";
                status = this.checkGame(newGameBoardState);
                if (status == FINISHED || status == TIE){
                    msg = "Finished";
                    finishedFlag = true;
                }
                this.setState({gameboard:newGameBoardState, next: newItem, message:msg, isFinished: finishedFlag, history:history, gameStatus: status})
                // console.log(newGameBoardState, number, newItem)
        }
    }
    renderStatus(){
        if(this.state.gameStatus == FINISHED){
            let wonPlayer = 'x';
            if (this.state.next == 'x')
                wonPlayer = 'o';
            return <div> player <b>{wonPlayer}</b> wins ! </div>
        }else if(this.state.gameStatus == RUNNING){
            return <div> next turn <b>{this.state.next}</b> </div>
        }else{
            return <b> Tie </b>
        }

    }
    checkGame(data){
        if( (data[0] === data[1] && data[1] === data[2] ) && data[1] != ""){
            return FINISHED;
        }else if( (data[3] === data[4] && data[4] === data[5] ) && data[4] != ""){
            return FINISHED;
        }else if( (data[6] === data[7] && data[7] === data[8] ) && data[7] != ""){
            return FINISHED;
        }else if( (data[0] === data[4] && data[4] === data[8] ) && data[4] != ""){
            return FINISHED;
        }else if( (data[2] === data[4] && data[4] === data[6] ) && data[4] != ""){
            return FINISHED;
        }else{
            for (let i in data){
                if (data[i] == '')
                    return RUNNING
            }
        }
        return TIE;
    }
    renderBoardItems(){
        let items = this.state.gameboard.map ((elt, i) =>
            <BoardItem key={i} currentItem={elt} number={i} updateItem={this.updateItem}/>
        )
        return items;
    }
    renderGameBoardHistoryState(){
        let items = this.state.history.map ((elt, i) =>{

            //console.log(elt);
            return (<tr key={i}>
                <td>{JSON.stringify(elt.state)}</td>
                <td>{elt.move}</td>
                <td>{elt.player}</td>
            </tr>)
        }
        )
        // console.log(items);
        return items;
    }
    saveTrainingData(){
        axios.post(BASE_URL+'/save', {data: JSON.stringify(this.state.history)}).then(function (response) {
            console.log(response);
        })
        .catch(function (error) {
            console.log(error);
        });
    }
    predict(){
        let data = {};
        let self = this;
        data.state = this.state.gameboard;
        data.player = this.state.next;
        axios.post(BASE_URL+'/predict', {data: JSON.stringify(data)}).then(function (response) {
            console.log(response);
            self.setState({debug:response.data.prediction});
            self.updateItem(response.data.prediction)
        })
        .catch(function (error) {
            console.log(error);
        });
    }
	render(){
        const itemWrapper = {
            display : "grid",
            gridTemplateColumns : "33% 33% 33%",
            width : "100px"
        }
        const wrapper = {
            display : "grid",
            gridTemplateColumns : "40% 20% 40%"
        }
        //this.renderBoardItems()
		return (
            <div>
                <div style={wrapper}>
                    <center >
                        {this.renderStatus()}
                        <button onClick={this.saveTrainingData}>Save</button>
                        <button onClick={this.predict}>Predict</button>

                    </center>
                    <center>
                        <div style={itemWrapper}> {this.renderBoardItems()} </div>

                    </center>
                    <div>
                        <table>
                            <tbody>
                                {this.renderGameBoardHistoryState()}
                            </tbody>
                        </table>
                    </div>
                    {JSON.stringify(this.state.debug)}
                </div>
            </div>
        );
	}
}
