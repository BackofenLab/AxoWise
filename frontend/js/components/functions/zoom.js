Vue.component("zoom",  {
    mounted: function() {
        $("#zoom").find("div.z").each(function () {
            var z = $(this);
            var rel = z.attr("rel");
            z.click(function () {
                if (rel == "center") {
                    sigma_instance.camera.goTo({
                        x: 0,
                        y: 0,
                        ratio: 1,
                        angle: sigma_instance.camera.angle
                    });
                } else {
                    sigma_instance.camera.goTo({
                        x: sigma_instance.camera.x,
                        y: sigma_instance.camera.y,
                        ratio: sigma_instance.camera.ratio * ("in" == rel ? 0.8 : 1.2),
                        angle: sigma_instance.camera.angle
                    });
                }
            })
        });
    },
    template: `
    <div id="zoom-parent">
        <div id="zoom">
            <div class="z" rel="in"></div>
            <div class="z" rel="out"></div>
            <div class="z" rel="center"></div>
        </div>
    </div>
    `
});