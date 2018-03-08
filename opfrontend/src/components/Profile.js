import React, {Component} from 'react';

import { OpalAPI } from '../utils/opal-api';

export default class Profile extends Component {
    constructor(props){
        super(props);

        this.state = {
            profile: {}
        };
    }

    componentDidMount() {
        let opalAPI = new OpalAPI();
        opalAPI.getUserInfo().then((data)=>{
            this.setState({
                profile: data
            });
        });
    }

    render(){
        return (
            <div>
            <pre>
                {JSON.stringify(this.state.profile)}
            </pre>
            </div>);
    }
}
