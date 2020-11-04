

# Front End:

## Adding a Vue Component:
### Creating the Component File
Create a new file componentName.js in frontend/js/components.
Eg:
~~~
Vue.component(“componentName”,{
props: [],
data: function() {},
methods: {},
template: ``
...
});
~~~
* props : pass data from a parent component down to it's child components.
* data : private memory of each component to store any variables needed
* methods: event handlers are written here
* template: bind the rendered DOM to the underlying Vue instance’s data. It is valid HTML. 
* watch:observe component data and run whenever a particular property changes

[Further reading in official documentation](https://vuejs.org/v2/api/)

### Registering the component for use:
In index.html, add 
~~~ 
<script src="js/components/componentName.js"></script> 
~~~
Set up the component for use by invoking it at the appropriate location and binding the desired data and events using v-directives.
~~~
<componentName></componentName> 
~~~

[Further reading on v-directives at Official Documentation](https://vuejs.org/v2/guide/syntax.html)

## Brief description of Vue Components:
* Visualisation- The display canvas contained in visualisation.js. Graph is rendered using the sigma js instance.
* Zoom
* Functional Enrichment
* Protein List- serves as the model of the tool, storing the protein list, as well as the values for the slider. Code stored in protein-list.js
* Search  
* Modules
* Attribute Pane - Loads more data about a selected protein.


