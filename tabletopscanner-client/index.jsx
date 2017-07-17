import * as React from "react";
import * as ReactDOM from "react-dom";
import Router from 'universal-router';
import {List} from "./components/list";
import {Index} from "./components/home";

const routes = [
    { path: '/', action: () => <Index/> },
    { path: '/search', action: () => <List items={[1, 2, 3, 4, 5]}/> },
    { path: '*', action: () => <h1>Not Found</h1> }
];

// Handle browser navigation events
let router = new Router(routes);

router.resolve({ path: window.location.pathname }).then(component => {
    ReactDOM.render(component, document.getElementById("root"));
});
