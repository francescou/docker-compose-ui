alertify.defaults = {
    // dialogs defaults
    autoReset:true,
    basic:false,
    closable:true,
    closableByDimmer:true,
    frameless:false,
    maintainFocus:true, // <== global default not per instance, applies to all dialogs
    maximizable:true,
    modal:true,
    movable:false,
    moveBounded:false,
    overflow:true,
    padding: true,
    pinnable:true,
    pinned:true,
    preventBodyShift:false, // <== global default not per instance, applies to all dialogs
    resizable:false,
    startMaximized:false,
    // transition:'pulse',

    // notifier defaults
    notifier:{
        // auto-dismiss wait time (in seconds)
        delay:5,
        // default position
        position:'bottom-right'
    },

    // language resources
    glossary:{
        // dialogs default title
        title:'docker-compose-ui',
        // ok button text
        ok: 'OK',
        // cancel button text
        cancel: 'Cancel'
    },

    // theme settings
    theme:{
        // class name attached to prompt dialog input textbox.
        input:'form-control',
        // class name attached to ok button
        ok:'btn btn-primary',
        // class name attached to cancel button
        cancel:'btn btn-default'
    }
};