new Vue({
  el: '#base',
  data: {
    isActive: false
  },
  methods: {
    closePopup: function() {
      this.isActive = true; 
    }
  },
  delimiters: ['[[',']]']
});
