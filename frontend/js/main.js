var sigInst, canvas, $GP

$(document).ready(function() {
    setupGUI()
});

function loadDataIntoSigma(json) {
    sigInst.graph.clear();
    sigInst.graph.read(json);
    sigInst.refresh();

}

function setupGUI() {
    // Submit button
    $("#submit-btn").click(function() {
        $("body").addClass("loading");
        $.post("api/subgraph/proteins", {
            proteins: $("#protein-list").val().split('\n').join(';'),
            // TODO threshold: threshold
        })
            .done(function (json) {
                $("body").removeClass("loading");
            loadDataIntoSigma(json);
        });
    });

    $GP = {
        calculating: !1,
        showgroup: !1
    };
    $GP.intro = $("#intro");
    $GP.minifier = $GP.intro.find("#minifier");
    $GP.mini = $("#minify");
    $GP.info = $("#attributepane");
    $GP.info_donnees = $GP.info.find(".nodeattributes");
    $GP.info_name = $GP.info.find(".name");
    $GP.info_link = $GP.info.find(".link");
    $GP.info_data = $GP.info.find(".data");
    $GP.info_close = $GP.info.find(".returntext");
    $GP.info_close2 = $GP.info.find(".close");
    $GP.info_p = $GP.info.find(".p");
    $GP.info_close.click(nodeNormal);
    $GP.info_close2.click(nodeNormal);
    $GP.form = $("#mainpanel").find("form");
    $GP.search = new Search($GP.form.find("#search"));

    initSigma();
}

function initSigma() {

    var a = new sigma();
    var cam = a.addCamera();

    a.addRenderer({
        container: "sigma-canvas",
        type: "canvas",
        camera: cam,
        settings: {
            defaultLabelColor: "#FFF",
            hideEdgesOnMove: true,
            maxEdgeSize: 0.3,
            minEdgeSize: 0.3,
            minNodeSize: 1,
            maxNodeSize: 10
        }
    });

    sigInst = a;
    a.active = !1;
    a.neighbors = {};
    a.detail = !1;

    sigInst.bind("clickNode", function (node) {
        nodeActive(node.data.node.id)
    });

    configSigmaElements();
}


// FUNCTION DECLARATIONS

Object.size = function(obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};



function configSigmaElements() {

    // $GP.bg = $(sigInst._core.domElements.bg);
    // $GP.bg2 = $(sigInst._core.domElements.bg2);
    var a = [],
        b,x=1;
        for (b in sigInst.clusters) a.push('<div style="line-height:12px"><a href="#' + b + '"><div style="width:40px;height:12px;border:1px solid #fff;background:' + b + ';display:inline-block"></div> Group ' + (x++) + ' (' + sigInst.clusters[b].length + ' members)</a></div>');
    //a.sort();
    // $GP.cluster.content(a.join(""));
    b = {
        minWidth: 400,
        maxWidth: 800,
        maxHeight: 600
    };//        minHeight: 300,
    $("a.fb").fancybox(b);
    $("#zoom").find("div.z").each(function () {
        var a = $(this),
            b = a.attr("rel");
        a.click(function () {
            if (b == "center") {
                sigInst.camera.goTo({
                    x: 0,
                    y: 0,
                    ratio: 1,
                    angle: sigInst.camera.angle
                })
                // sigInst.position(0,0,1).draw();
            } else {
                sigInst.camera.goTo({
                    x: sigInst.camera.x,
                    y: sigInst.camera.y,
                    ratio: sigInst.camera.ratio * ("in" == b ? 0.5 : 1.5 ),
                    angle: sigInst.camera.angle
                })
                // sigInst.zoomTo(a.domElements.nodes.width / 2, a.domElements.nodes.height / 2, a.mousecaptor.ratio * ("in" == b ? 1.5 : 0.5));
            }

        })
    });
    $GP.mini.click(function () {
        $GP.mini.hide();
        $GP.intro.show();
        $GP.minifier.show()
    });
    $GP.minifier.click(function () {
        $GP.intro.hide();
        $GP.minifier.hide();
        $GP.mini.show()
    });
    $GP.intro.find("#showGroups").click(function () {
        !0 == $GP.showgroup ? showGroups(!1) : showGroups(!0)
    });

    $GP.search.exactMatch = !0, $GP.search.search(a)
    $GP.search.clean();

}

function Search(a) {
    this.input = a.find("input[name=search]");
    this.state = a.find(".state");
    this.results = a.find(".results");
    this.exactMatch = !1;
    this.lastSearch = "";
    this.searching = !1;
    var b = this;
    this.input.focus(function () {
        var a = $(this);
        a.data("focus") || (a.data("focus", !0), a.removeClass("empty"));
        b.clean()
    });
    this.input.keydown(function (a) {
        if (13 == a.which) return b.state.addClass("searching"), b.search(b.input.val()), !1
    });
    this.state.click(function () {
        var a = b.input.val();
        b.searching && a == b.lastSearch ? b.close() : (b.state.addClass("searching"), b.search(a))
    });
    this.dom = a;
    this.close = function () {
        this.state.removeClass("searching");
        this.results.hide();
        this.searching = !1;
        this.input.val("");//SAH -- let's erase string when we close
        nodeNormal()
    };
    this.clean = function () {
        this.results.empty().hide();
        this.state.removeClass("searching");
        this.input.val("");
    };
    this.search = function (a) {
        var b = !1,
            c = [],
            b = this.exactMatch ? ("^" + a + "$").toLowerCase() : a.toLowerCase(),
            g = RegExp(b);
        this.exactMatch = !1;
        this.searching = !0;
        this.lastSearch = a;
        this.results.empty();
        if (2 >= a.length) this.results.html("<i>You must search for a name with a minimum of 3 letters.</i>");
        else {
            sigInst.graph.nodes().forEach(function (a) {
                g.test(a.label.toLowerCase()) && c.push({
                    id: a.id,
                    name: a.label
                })
            });
            if (c.length) {
                b = !0;
                nodeActive(c[0].id);
            }
            a = ["<b>Search Results: </b>"];
            if (1 < c.length) for (var d = 0, h = c.length; d < h; d++) a.push('<a href="#' + c[d].name + '" onclick="nodeActive(\'' + c[d].id + "')\">" + c[d].name + "</a>");
            0 == c.length && !b && a.push("<i>No results found.</i>");
            1 < a.length && this.results.html(a.join(""));
           }
        if(c.length!=1) this.results.show();
        if(c.length==1) this.results.hide();
    }
}

function showGroups(a) {
    a ? ($GP.intro.find("#showGroups").text("Hide groups"), /*$GP.bg.show(), $GP.bg2.hide(),*/ $GP.showgroup = !0) : ($GP.intro.find("#showGroups").text("View Groups"), /*$GP.bg.hide(), $GP.bg2.show(),*/ $GP.showgroup = !1)
}

function nodeNormal() {
    // !0 != $GP.calculating && !1 != sigInst.detail && (showGroups(!1), $GP.calculating = !0, sigInst.detail = !0, $GP.info.delay(400).animate({width:'hide'},350)
    sigInst.graph.edges().forEach(function (a) {
        a.hidden = false;
    });
    sigInst.graph.nodes().forEach(function (a) {
        a.hidden = false;
    });
    $GP.info.delay(400).animate({width:'hide'}, 350);
    $GP.calculating = !1;
    sigInst.neighbors = {};
    sigInst.refresh();
    sigInst.active = false;
}

sigma.classes.graph.addMethod('getNodeFromIndex', function(id) {
    return this.nodesIndex[id];
  });

function nodeActive(id) {

    sigInst.neighbors = {};
    sigInst.detail = !0;
    var node = sigInst.graph.getNodeFromIndex(id);

    showGroups(!1);

    var outgoing = {}, incoming = {}, mutual = {};

    sigInst.graph.edges().forEach(function (e) {
        e.hidden = true;

        n = {
            name: e.label,
            color: e.color
        };

        if (id == e.source)
            outgoing[e.target] = n;
        else if (id == e.target)
            incoming[e.source] = n;

        if (id == e.source || id == e.target)
            sigInst.neighbors[id == e.target ? e.source : e.target] = n;

        e.hidden = false;
    });

    var f = [];

    // Hide all nodes first
    sigInst.graph.nodes().forEach(function (n) {
        n.hidden = true;
    });

    var createList = function(ids) { // dict
        var lis = [];
        var e = [];
        for (var id_ in ids) {
            var n = sigInst.graph.getNodeFromIndex(id_);
            n.hidden = false;
            if (id != id_) e.push({
                id: id_,
                name: n.label,
                color: ids[id_].color
            })
        }

        e.sort(function (a, b) {
            var name_a = a.name.toLowerCase(),
                name_b = b.name.toLowerCase();
            return name_a < name_b ? -1 : name_a > name_b ? 1 : 0;
        });

        for (g in e) {
            c = e[g];
            lis.push('<li class="membership"><a href="#' + c.name + '"  onclick=\"nodeActive(\'' + c.id + '\')">' + c.name + "</a></li>");
        }
        return lis;
    }

    /*console.log("mutual:");
    console.log(mutual);
    console.log("incoming:");
    console.log(incoming);
    console.log("outgoing:");
    console.log(outgoing);*/


    var f=[];

    f = f.concat(createList(sigInst.neighbors));

    // node is object of active node
    node.hidden = false;
    node.color = node.color;
    node.lineWidth = 6;
    node.strokeStyle = "#000000";
    sigInst.refresh()

    $GP.info_link.find("ul").html(f.join(""));
    $GP.info_link.find("li").each(function () {
        var a = $(this),
            b = a.attr("rel");
    });
    f = node;
    if (f.attributes) {
          var image_attribute = false;
        e = [];
        temp_array = [];
        g = 0;
        for (var attr in f.attributes) {
            var d = f.attributes[attr],
                h = "";
            if (attr!=image_attribute) {
                h = '<span><strong>' + attr + ':</strong> ' + d + '</span><br/>'
            }
            //temp_array.push(f.attributes[g].attr);
            e.push(h)
        }

        $GP.info_name.html("<div><span>" + node.label + "</span></div>");
        $GP.info_data.html(e.join("<br/>"))
    }
    $GP.info_data.show();
    $GP.info_p.html("Connections:");
    $GP.info.animate({width:'show'},350);
    $GP.info_donnees.hide();
    $GP.info_donnees.show();
    sigInst.active = id;
}

