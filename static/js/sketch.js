
// Helper Functions
function enable(element, enable) {
    if (enable) {
        $(element).removeClass("disabled");
    } else {
        $(element).addClass("disabled");
    }
}

function select(element1, element2) {
    $(element1).addClass("selected");
    $(element2).removeClass("selected");
}

// Initialize Raphael Sketchpad
var sketchpad = Raphael.sketchpad("editor", {
    height: "400",
    width: "600",
    editing: true	// true is default
});

// Event Handler for Colorpicker
$('#colorpicker').colorpicker().on('changeColor', function(ev){
    sketchpad.pen().color(ev.color.toHex());
});

// Undo/Redo
$("#editor_undo").click(function() {
    sketchpad.undo();
});
$("#editor_redo").click(function() {
    sketchpad.redo();
});

// Clear Drawing
$("#editor_clear").click(function() {
    sketchpad.clear();
});

// Marker Sizes
$("#editor_tiny").click(function() {
    sketchpad.pen().width(2);
});
$("#editor_small").click(function() {
    sketchpad.pen().width(10);
});
$("#editor_medium").click(function() {
    sketchpad.pen().width(15);
});
$("#editor_large").click(function() {
    sketchpad.pen().width(20);
});
$("#editor_huge").click(function() {
    sketchpad.pen().width(25);
});

// Marker Opacity
$("#editor_solid").click(function() {
    select("#editor_solid", "#editor_fuzzy");
    sketchpad.pen().opacity(1);
});
$("#editor_fuzzy").click(function() {
    select("#editor_fuzzy", "#editor_solid");
    sketchpad.pen().opacity(0.3);
});

// Eraser
$("#editor_erase").click(function() {
    select("#editor_erase","#editor_pen");
    sketchpad.editing("erase");
});

// Pen
$("#editor_pen").click(function() {
    select("#editor_pen", "#editor_erase");
    sketchpad.editing(true);
});


$("#editor_draw_erase").toggle(function() {
    sketchpad.editing("erase");
}, function() {
    $(this).text("Draw");
    sketchpad.editing(true);
});

function update_actions() {
    enable("#editor_undo", sketchpad.undoable());
    enable("#editor_redo", sketchpad.redoable());
    enable("#editor_clear", sketchpad.strokes().length > 0);
}

sketchpad.change(update_actions);

update_actions();
