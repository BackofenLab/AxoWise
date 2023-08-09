    import  sigma  from "sigma";
    import {emitter} from "../main.js"

    /**
     * This method resizes each DOM elements in the container and stores the new
     * dimensions. Then, it renders the graph.
     *
     * @param  {?number}                width  The new width of the container.
     * @param  {?number}                height The new height of the container.
     * @return {sigma.renderers.canvas}        Returns the instance itself.
     */
    sigma.renderers.canvas.prototype.resize = function(w, h) {
      emitter.emit('resizeCircle')
      var k,
          oldWidth = this.width,
          oldHeight = this.height,
          pixelRatio = sigma.utils.getPixelRatio();
  
      if (w !== undefined && h !== undefined) {
        this.width = w;
        this.height = h;
      } else {
        this.width = this.container.offsetWidth;
        this.height = this.container.offsetHeight;
  
        w = this.width;
        h = this.height;
      }
  
      if (oldWidth !== this.width || oldHeight !== this.height) {
        for (k in this.domElements) {
          this.domElements[k].style.width = w + 'px';
          this.domElements[k].style.height = h + 'px';
  
          if (this.domElements[k].tagName.toLowerCase() === 'canvas') {
            this.domElements[k].setAttribute('width', (w * pixelRatio) + 'px');
            this.domElements[k].setAttribute('height', (h * pixelRatio) + 'px');
  
            if (pixelRatio !== 1)
              this.contexts[k].scale(pixelRatio, pixelRatio);
          }
        }
      }
  
      return this;
    };