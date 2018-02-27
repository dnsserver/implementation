import React, {Component} from 'react';
import {Link} from 'react-router-dom';

import { OpalAPI } from '../utils/opal-api';

export default class Client extends Component {
    constructor(props){
        super(props);
        const cfg = JSON.parse(this.props.config);
        this.state = {
            orns: [],
            config: cfg
        };
    }

    componentDidMount() {
        let opalAPI = new OpalAPI();
        opalAPI.getOpalResourceList(this.state.config.opal_data_provider, 'orn').then((data)=>{
            this.setState({
                orns: data
            });
        });
    }

    render(){
        const orns = this.state.orns || [];
        return (
            <div className="row">
                    <div className="col-sm-12">
                        Connection Requests:
                    </div>
                    <div className="col-sm-12">
                        <div className="list-group">
                        {orns.map((o) => {
                            return (
                                <div key={o.id} className="list-group-item">
                                    {o.id}: {o.name} - {o.description}
                                </div>
                            );
                        })}
                        </div>
                    </div>
                </div>
        );
    }
}
