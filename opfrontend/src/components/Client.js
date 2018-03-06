import React, {Component} from 'react';
import {Link} from 'react-router-dom';
import {NotificationManager} from 'react-notifications';

import { OpalAPI } from '../utils/opal-api';

export default class Client extends Component {
    constructor(props){
        super(props);
        const sess = JSON.parse(sessionStorage.getItem('session'));
        const cfg = JSON.parse(sessionStorage.getItem('config'));
        this.state = {
            orns: [],
            config: cfg,
            session: sess,
            // Properties for the PersonaProvider registration
            name: '',
            description: '',
            recurring: false,
            scopes: [],
            result_url: ''
        };
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleInputChange = this.handleInputChange.bind(this);
        this.handleScopeChange = this.handleScopeChange.bind(this);
    }

    handleSubmit(e){
        e.preventDefault();
        const config = this.state.config;
        const session = this.state.session;
        let scopes = this.state.scopes;

        let pp = {
            "redirect_uris": [
                config.base_url + "/opal_oidc/"+this.state.name
            ],
            "client_name": this.state.name,
            "token_endpoint_auth_method": "client_secret_post",
            "scopes": scopes,
            "grant_types": [
                "authorization_code"
            ],
            "response_types": [
                "code"
            ],
            "jwksType": "URI",
            "default_max_age": 60000,
            "require_auth_time": true,
            "description":this.state.description,
            "recurring":this.state.recurring,
            "result_url":this.state.result_url
        }
        console.log(pp);
        let opalAPI = new OpalAPI();
        opalAPI.registerClient(config.opal_data_provider, session.access_token, pp).then((data)=>{
            console.log(data);
            NotificationManager.info("Client registered.", '', 3000);
        });
    }

    handleInputChange(event) {
        const target = event.target;
        const value = target.type === 'checkbox' ? target.checked : target.value;
        const name = target.name;
        this.setState({
            [name]: value
        });
    }

    handleScopeChange(event){
        const target = event.target;
        const options = target.options;

        let scopes = [];
        for (var i = 0, l = options.length; i < l; i++) {
            if (options[i].selected) {
                scopes.push(options[i].value);
            }
        }
        this.setState({
            "scopes": scopes
        });
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
                    <form onSubmit={this.handleSubmit}>
                        <div className="form-group">
                            <label htmlFor="name">Name</label>
                            <input type="text" className="form-control"
                                id="name" name="name" required={true}
                                value={this.state.name}
                                onChange={this.handleInputChange} />
                        </div>
                        <div className="form-group">
                            <label htmlFor="description">Description</label>
                            <textarea className="form-control"
                                id="description" name="description"
                                required={true}
                                value={this.state.description}
                                onChange={this.handleInputChange}/>
                        </div>
                        <div className="form-group">
                            <label className="form-control">
                                <input type="checkbox"
                                    name="recurring"
                                    value={this.state.recurring}
                                    onChange={this.handleInputChange} />
                                &nbsp; Recurring Job
                            </label>
                        </div>
                        <div className="form-group">
                            <label htmlFor="result_url">Result URL</label>
                            <input type="text" className="form-control"
                                id="result_url" name="result_url"
                                value={this.state.result_url}
                                onChange={this.handleInputChange} />
                        </div>
                        <div className="form-group">
                            <label htmlFor="scopes">Scopes</label>
                            <select className="form-control"
                                id="scopes" name="scopes"
                                multiple={true}
                                required={true}
                                value={this.state.scopes}
                                onChange={this.handleScopeChange}>
                            {orns.map((o) => {
                                return (
                                    <option key={o.id} value={o.id}>{o.name}</option>
                                );
                            })}
                            </select>

                        </div>
                        <button type="submit" className="btn btn-default">Register</button>
                    </form>
                </div>
            </div>
        );
    }
}
