new Vue({
  el: '#moneypit-event-log',
  data: {
    device: '',
    location: '',
    events: []
  },

  methods: {

  },

  created () {
    var vm = this;

    axios.get('./api/config')
    .then(function (response) {
      vm.device = response.data.device;
      vm.location = response.data.location;
    })

    axios.get('./api/events')
    .then(function (response) {
      response.data.forEach(function(v,k) {
        vm.events.push(v);
      });
    })

  }
})
