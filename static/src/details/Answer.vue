<template>
  <div class="table-responsive" v-if="files">
    <div class="form-label">Fichier{{ answer_count===1 ? '': 's' }} déposé{{ answer_count===1 ? '': 's' }}:</div>
    <table class="table table-hover table-outline table-vcenter text-nowrap card-table">
      <thead>
        <tr>
          <th class="text-center w-1"></th>
          <th>Date de dépôt</th>
          <th>Nom du document</th>
          <th class="text-center">Déposant</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="file in files" :key="file.id">
          <td class="text-center">
            <div class="fe fe-file"></div>
          </td>
          <td>
            <div>{{  file.creation_date }}</div>
            <div class="small text-muted">{{  file.creation_time }}</div>
          </td>
          <td>
            <div><a target="_blank" :href="file.url">{{ file.basename }}</a></div>
          </td>
          <td class="text-center">
            <div>{{ file.author.first_name }} {{ file.author.last_name }}</div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>

  import Vue from "vue";

  export default Vue.extend({
    data() {
      return {answer_count: 0, files: {}};
    },
    mounted() {
      var _this = this
      this.$parent.$on('answer-updated-' + this.question_id, function (files) {
        _this.files = files;
      })
    },
    computed: {
      answer_count: function () {
         return files ? this.files.length: 0;
      }
    },
    props: {
      question_id: String,
    },
    methods: {}
  });
</script>

<style scoped>

</style>