import React, {Component} from 'react';
import {Link} from 'react-router-dom';

export default class Client extends Component {
    constructor(props){
        super(props);
        this.state = {};
    }

    render(){
        return (
            <div className="row">
                    <div className="col-sm-12">
                        Connection Requests:
                    </div>
                    <div className="col-sm-12">
                        <div className="list-group">

                                    <div  className="list-group-item">
                                        None
                                    </div>

                        </div>
                    </div>
                </div>
        );
    }
}
