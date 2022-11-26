<template>
  <v-container>
    <v-layout>
      <v-row justify="center">
        <v-col cols="8">
          <v-card min-height="800" color="#f5efe6">
            <v-card-title id="title1" class="pt-16 pl-16 pb-10">
              냉장고
            </v-card-title>
            <v-layout>
              <v-row justify="center">
                <v-col cols="10">
                  <v-card height="500">
                    <v-row justify="space-between">
                      <v-card-title id="title2" class="pl-10">
                        보유 재료
                      </v-card-title>
                      <v-btn round color="#7895b2" dark class="mt-4 mr-10" @click="showAddIngredientDialog">재료추가</v-btn>
                    </v-row>
                    
                    <!-- 여기서부턴 vfor 문법을 사용해서 무한 리스트를 만들어야 합니다. -->
                    
                  </v-card>
                </v-col>
              </v-row>  
            </v-layout>
          </v-card>
        </v-col>
      </v-row>
    </v-layout>

    <!-- 재료 추가 팝업창 -->
    <v-dialog
      max-width="500"
      v-model="addIngredientDialog"
    >
      <add-ingredient-dialog
        @add="add"
        @hide="hideAddIngredientDialog"
      />
    </v-dialog>

  </v-container>
</template>

// Pagination

<script>
import herokuAPI from '@/api/heroku.js';
import AddIngredientDialog from '@/components/addIngredient.vue'

export default{
  components: {
    AddIngredientDialog
  },
  data(){
    return{
      addIngredientDialog: false,
      refrigerators: [],
    }
  },
  mounted() {
    // 냉장고 조회 - 원래 mounted 에 있어야 하는 놈 
    const UserInfo = JSON.parse(localStorage.getItem("UserInfo"));
    let vm = this;
    herokuAPI.refrigeratorLookup(UserInfo.nickname)
      .then(function(response) {
        console.log("응답 온거", response);
        if(response.status == 200) {
            console.log("조회 성공");
            for(let i = 0; response.data[i] != null; i++) {
              vm.refrigerators.push(response.data[i]);
            }
          }
      })
      
  },
  methods: {
    showAddIngredientDialog() {
      this.addIngredientDialog = true;
    },
    hideAddIngredientDialog() {
      this.addIngredientDialog = false;
    },
    add(ingredient) {
      this.refrigerators.push(ingredient);
    },
    deleteRefrigerator() {
      const deleteTarget = JSON.stringify (
        {
          "id": 3
        }
      );
      herokuAPI.refrigeratorDelete(deleteTarget)
        .then(function(response) {
          console.log("응답 온거", response);
          if(response.status == 200) {
            console.log("삭제 성공");
          }
        })
    },
    updateRefrigerator() {
      const edittedTarget = JSON.stringify({
        "id": 1,
        "amount": 1000,
        "expiry_date": '2022-12-31',
        "name": "kkochu",
        "nickname": "test",
        "unit": "g"
      });
      herokuAPI.refrigeratorEdit(edittedTarget)
        .then(function(response) {
          console.log("응답 온거", response);
          if(response.status == 200) {
            console.log("수정 성공");
          }
        })
    },
    
  }
}
</script>

<style>
  #title1{
    font-size: 2em;
    color: #7895b2;
  }
  #title2{
    font-size: 1.4em;
    color: #7895b2;
  }
</style>