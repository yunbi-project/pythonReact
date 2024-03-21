import React from "react";
import "../styles/common/main.css"

class Main extends React.Component {
    changeText(e){
        let file = e.target.files[0];
        let fileReader = new FileReader();
        fileReader.onload = () => {
          console.log(fileReader.result);
        };
        fileReader.readAsText(file);
      }

    render() {
        return (
            <div className="Main">
                <header className="Main-header">
                    <p>{this.state.text}</p>
                </header>
                <div className="btn-container">
                    <button className="btn" onClick={this.changeText}>
                        <p>my python</p>
                    </button>
                </div>
            </div>
        );
    }
}

export default Main;