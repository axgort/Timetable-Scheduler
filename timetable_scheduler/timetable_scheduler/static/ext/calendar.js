/*!
 * Extensible 1.5.2
 * Copyright(c) 2010-2013 Extensible, LLC
 * licensing@ext.ensible.com
 * http://ext.ensible.com
 */
Ext.Loader.setConfig({
    enabled: true,
    disableCaching: false,
    paths: {
        "Extensible": "src",
        "Extensible.example": "examples/"
    }
});
Ext.require([
    'Ext.data.proxy.Rest',
    'Extensible.calendar.data.MemoryCalendarStore',
    'Extensible.calendar.data.EventStore',
    'Extensible.calendar.CalendarPanel'
]);


Ext.define('Extensible.example.calendar.DummyCalendar', {
    constructor: function() {
        return {
            "calendars" : [{
                "id"    : 1,
                "title" : "Home",
                "color" : 2
            }]
        };
    }
});
Ext.onReady(function(){

    var calendarStore = Ext.create('Extensible.calendar.data.MemoryCalendarStore', {
		/*
        autoLoad: true,
        proxy: {
            type: 'ajax',
            url: 'http://ext.ensible.com/deploy/dev/examples/calendar/data/calendars.json',
            noCache: false,
            
            reader: {
                type: 'json',
                root: 'calendars'
            }

        }
        */
        
    });
    
    var eventStore = Ext.create('Extensible.calendar.data.EventStore', {
        autoLoad: true,
        proxy: {
            type: 'rest',
            //url: 'http://ext.ensible.com/deploy/dev/examples/calendar/remote/php/app.php/events',
            url: document.URL+'json/',
            noCache: false,
            
            reader: {
                type: 'json',
                root: 'data'
            },
            
            writer: {
                type: 'json',
                nameProperty: 'mapping'
            },
            
            listeners: {
                exception: function(proxy, response, operation, options){
                    var msg = response.message ? response.message : Ext.decode(response.responseText).message;
                    // ideally an app would provide a less intrusive message display
                    Ext.Msg.alert('Server Error', msg);
                }
            }
            
        },

        // It's easy to provide generic CRUD messaging without having to handle events on every individual view.
        // Note that while the store provides individual add, update and remove events, those fire BEFORE the
        // remote transaction returns from the server -- they only signify that records were added to the store,
        // NOT that your changes were actually persisted correctly in the back end. The 'write' event is the best
        // option for generically messaging after CRUD persistence has succeeded.
        listeners: {
            'write': function(store, operation){
                var title = Ext.value(operation.records[0].data[Extensible.calendar.data.EventMappings.Title.name], '(No title)');
                switch(operation.action){
                    case 'create': 
                        Extensible.example.msg('Add', 'Added "' + title + '"');
                        break;
                    case 'update':
                        Extensible.example.msg('Update', 'Updated "' + title + '"');
                        break;
                    case 'destroy':
                        Extensible.example.msg('Delete', 'Deleted "' + title + '"');
                        break;
                }
            }
        }
		});
    
    var cp = Ext.create('Extensible.calendar.CalendarPanel', {
        id: 'calendar-remote',
        eventStore: eventStore,
        calendarStore: calendarStore,
        renderTo: 'cal',
        title: 'Remote Calendar',
        width: 900,
        height: 700,
        showDayView: false,
        showMonthView: false,
        showMultiWeekView: false
    });
       
});
