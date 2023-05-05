import sigma from "sigma";

export default function saveAsPNG(renderer, params, mode) {

  // Constants
  var CONTEXTS = ['scene', 'edges', 'nodes', 'labels'],
  TYPES = {
    png: 'image/png',
    jpg: 'image/jpeg',
    gif: 'image/gif',
    tiff: 'image/tiff'
  };
  // Main function
  params = params || {};
  mode = mode || "black";
  
  // Enforcing
  if (params.format && !(params.format in TYPES))
  throw Error('sigma.renderers.snaphot: unsupported format "' +
  params.format + '".');
  
  var self = renderer.renderers[0],
  webgl = this instanceof sigma.renderers.webgl,
  doneContexts = [];

  if(mode == 'white') {
    self.settings({defaultLabelColor: '#000'});
    renderer.refresh()
  }
  
  // Creating a false canvas where we'll merge the other
  var merged = document.createElement('canvas'),
      mergedContext = merged.getContext('2d'),
      sized = false;

  // Iterating through context
  CONTEXTS.forEach(function(name) {
    if (!self.contexts[name])
      return;

    if (params.labels === false && name === 'labels')
      return;

    var canvas = self.domElements[name] || self.domElements['scene'],
        context = self.contexts[name];

    if (~doneContexts.indexOf(context))
      return;

    if (!sized) {
      merged.width = webgl && context instanceof WebGLRenderingContext ?
       canvas.width / 2 :
       canvas.width;
      merged.height = webgl && context instanceof WebGLRenderingContext ?
        canvas.height / 2 :
        canvas.height
      sized = true;

      // Do we want a background color?
      if (params.background) {
        mergedContext.rect(0, 0, merged.width, merged.height);
        mergedContext.fillStyle = params.background;
        mergedContext.fill();
      }
    }

    if (context instanceof WebGLRenderingContext)
      mergedContext.drawImage(canvas, 0, 0,
        canvas.width / 2, canvas.height / 2);
    else
      mergedContext.drawImage(canvas, 0, 0);

    doneContexts.push(context);
  });

  var dataUrl = merged.toDataURL(TYPES[params.format || 'png']);

  self.settings({defaultLabelColor: '#FFF'});
  console.log(self)
  renderer.refresh()

  if (params.download)
    download(
      dataUrl,
      params.format || 'png',
      params.filename
    );

  return dataUrl;

  // Utilities
function download(dataUrl, extension, filename) {

  // Anchor
  var anchor = document.createElement('a');
  anchor.setAttribute('href', dataUrl);
  anchor.setAttribute('download', filename || 'graph.' + extension);

  // Click event
  var event = document.createEvent('MouseEvent');
  event.initMouseEvent('click', true, false, window, 0, 0, 0 ,0, 0,
    false, false, false, false, 0, null);

  anchor.dispatchEvent(event);
}
}