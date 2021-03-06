import 'babel-polyfill'
import { mapActions } from 'vuex'
import Vue from 'vue/dist/vue.js'
import Vuex from 'vuex'

import { store } from "./store"
import AddUserModal from "./users/AddUserModal"
import RemoveUserModal from "./users/RemoveUserModal"
import UpdateUserModal from "./users/UpdateUserModal"
import Users from './users/Users'

Vue.use(Vuex);

new Vue({
  store,
  el: '#questionnaire-list-vm',
  data: {
  },
  components: {
    'users-for-control': Users,
    AddUserModal,
    UpdateUserModal,
    RemoveUserModal
  },
  methods: {
    ...mapActions(['setSessionUser'])
  },
  created() {
    this.setSessionUser()
  }
});
