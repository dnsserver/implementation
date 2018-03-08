import React, {Component} from 'react';
import {NotificationManager} from 'react-notifications';

import { OpalAPI } from '../utils/opal-api';

export default class OpalClient extends Component {
    constructor(props){
        super(props);
        const cfg = JSON.parse(sessionStorage.getItem('config'));
        this.state = {
            config: cfg,
            name: null,
            description: null,
            oidc_request: null,
            oidc_response: null
        };

    }

    componentDidMount() {
        const config = this.state.config;
        if(this.props.match.params.id){

            const id = this.props.match.params.id;
            const opalAPI = new OpalAPI();

            const params = new URLSearchParams(this.props.location.search);
            const code = params.get('code');
            const error = params.get('error');
            const error_description = params.get('error_description');

            opalAPI.getClient(id).then((data)=>{
                const name = data["name"];
                const desc = data["description"];
                const oidc_request = JSON.parse(data["oidc_request"]);
                const oidc_response= JSON.parse(data["oidc_response"]);
                this.setState({
                    name: name,
                    description: desc,
                    oidc_request: oidc_request,
                    oidc_response: oidc_response
                });
                const client_cfg = {
                    "token_uri":config.token_uri,
                    "auth_uri":config.auth_uri,
                    "redirect_uri": oidc_response["redirect_uris"][0],
                    "client_id":oidc_response["client_id"],
                    "client_secret":oidc_response["client_secret"],
                    "scopes":oidc_response["scope"]
                }

                if(code){
                    opalAPI.getAccessToken(client_cfg, code).then((data)=>{
                        console.log(data);
                        NotificationManager.info("Client approved.", '', 3000);
                    }).catch((error)=>{
                        let msg = error.message;
                        if(error && error.response && error.response.data &&
                            error.response.data.error_description){
                                msg = error.response.data.error_description;
                        }
                        NotificationManager.error(msg, '', 3000);
                    });
                }else if(error){
                    NotificationManager.error(error_description, '', 3000);
                }else{
                    opalAPI.redirectForLogin(client_cfg, oidc_response["redirect_uris"][0]);
                }
                //console.log(client_cfg);
            });

        }
    }

    render(){
        return (
            <div>
                <p>OPAL Client</p>
                <div className="row">
                    <div className="col-sm-12">
                        <h5 className="mb-1">{this.state.name}</h5>
                        <small className="text-muted">{this.state.description}</small>
                    </div>
                    <div className="col-sm-12">
                        <pre>
                            {JSON.stringify(this.state.oidc_request, null, "  ")}
                        </pre>
                    </div>
                    <div className="col-sm-12">
                        <pre>
                            {JSON.stringify(this.state.oidc_response, null, "  ")}
                        </pre>
                    </div>
                </div>
            </div>);
    }
}
