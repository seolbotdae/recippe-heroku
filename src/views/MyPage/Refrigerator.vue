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
                  <v-card>
                    <v-row justify="space-between">
                      <v-card-title id="title2" class="pl-10">
                        보유 재료
                      </v-card-title>
                      <v-btn round color="#7895b2" dark class="mt-4 mr-10" @click="showAddIngredientDialog">재료추가</v-btn>
                    </v-row>

                    <!-- 재료 없는 경우 -->
                    <v-card-text v-if="isEmpty">보유 재료가 없습니다.</v-card-text>
                  
                    <!-- 재료 있는 경우 -->
                    <v-card-text v-if="!isEmpty">
                      <!-- 재료 v card -->
                      <v-card v-for="item in refrigerators" :key="item" outlined>
                        <!-- 윗줄 -->
                        <div class="d-flex justify-space-between">
                          <span class="ml-3">{{item.name}}</span>
                          <span class="mr-3">{{item.amount}}{{item.unit}}</span>
                        </div>

                        <!-- 구분선 -->
                        <v-divider />

                        <!-- 아랫줄 -->
                        <div class="d-flex justify-space-between">
                          <span class="ml-3">{{item.expiry_date}}</span>
                          <div class="mr-3">
                            <v-btn>수정하기</v-btn>
                            <v-btn @click="deletePopup(item.id)">삭제하기</v-btn>
                          </div>
                        </div>
                        
                      </v-card>
                    </v-card-text>
                    
                  </v-card>
                </v-col>
              </v-row>  
            </v-layout>
          </v-card>
        </v-col>
      </v-row>
    </v-layout>

    <!-- 팝업창 형식 -->
    <v-dialog
      max-width="300"
      v-model="popupDialog"
    >
      <popup-dialog
        :headerTitle=headerTitle
        :btn1Title=btn1Title
        :btn2Title=btn2Title
        :btn2=btn2
        @hide="hideDialog"
        @submit="deleteIngre"
      >
        <template v-slot:body>
          <!-- 내용이 들어가는 부분입니다아 -->
          <div>{{ content1 }}</div>
        </template>
      </popup-dialog>
    </v-dialog>

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
import PopupDialog from '@/components/popup.vue';
import AddIngredientDialog from '@/components/addIngredient.vue';

export default{
  components: {
    PopupDialog,
    AddIngredientDialog
  },
  data(){
    return{
      popupDialog: false,
      headerTitle: "",
      content1: "",
      btn1Title: "",
      btn2Title: "",
      btn2: false,
      id: -1,
      addIngredientDialog: false,
      refrigerators: [],
      isEmpty: false,
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
      .catch(function (e) {
        if(e.response.status == 401) {
          console.log("조회 실패");
          vm.requestFailPopup();
        } else if(e.response.status == 404) {
          console.log("404 식재료 없음");
          vm.isEmpty = true;
        } else if(e.response.status == 500) {
          console.log("500 Unknown error");
          vm.requestFailPopup();
        }
      });
  },
  methods: {
  // 팝업창 메소드들
    showDialog() { // 팝업창 보이기
      this.popupDialog = true;
    },
    hideDialog() { // 팝업창 숨기기
      this.popupDialog = false;
    },
    deletePopup(click_id) {
      this.headerTitle = "재료 삭제";
      this.content1 = "해당 식재료를 삭제하시겠습니까?";
      this.btn1Title = "취소";
      this.btn2Title = "삭제";
      this.btn2 = true;
      this.id = click_id;
      this.showDialog();
    },
    deleteFailPopup() {
      this.headerTitle = "재료 삭제 실패";
      this.content1 = "재료 삭제에 실패했습니다.";
      this.btn1Title = "확인";
      this.btn2 = false;
      this.showDialog();
    },
    requestFailPopup() {
      this.headerTitle = "보유 재료 불러오기 실패";
      this.content1 = "보유 재료 조회에 실패했습니다.";
      this.btn1Title = "확인";
      this.btn2 = false;
      this.showDialog();
    },
    deleteIngre() {
      const deleteTarget = JSON.stringify ({ "id": this.id });
      herokuAPI.refrigeratorDelete(deleteTarget)
        .then(function(response) {
          console.log("응답 온거", response);
          if(response.status == 200) {
            console.log("삭제 성공");
          }
        })
        .catch(function (e) {
        if(e.response.status == 406) {
          console.log("406 삭제 실패");
          vm.deleteFailPopup();
        } else if(e.response.status == 500) {
          console.log("500 Unknown error");
          vm.deleteFailPopup();
        }
      });
    },

  // 재료추가 팝업창 메소드들
    showAddIngredientDialog() {
      this.addIngredientDialog = true;
    },
    hideAddIngredientDialog() {
      this.addIngredientDialog = false;
    },
    add(ingredient) {
      this.refrigerators.push(ingredient);
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