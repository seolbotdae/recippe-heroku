<template>
  <v-card>
    <!-- 재료 입력 부분 -->
    <v-card-text>

      <div style="color:#7895B2; font-size: 2.1em;" class="py-6">
        보유 재료 수정
      </div>

      <div style="color:#7895B2; font-size: 1.3em;">
        내용 수정
      </div>

      <div class="searchbox mb-6">
        <div class="header">
          <v-text-field
            class="mx-6"
            v-model="name"
            disabled
          ></v-text-field>
        </div>
      </div>
      
      <div style="color:#7895B2; font-size: 1.3em;">
        수량
      </div>

      <v-text-field
        placeholder="수량 입력"
        hide-details="auto"
        id="inputText"
        class="mx-6 mb-8"
        v-model="amount"
      ></v-text-field>

      <div style="color:#7895B2; font-size: 1.3em;">
        단위
      </div>

      <v-text-field
        placeholder="단위 입력"
        id="inputUnit"
        @click="units_filter"
        class="mx-6 mb-0"
        v-model="unit"
      ></v-text-field>

      <div class="units-container mx-6">
        <div v-for="i in units" :key="i.name">
          <span ref="unitsName" class="unitsName visible" @click="clickUnit">{{i.name}}</span>
        </div>
        <div class="mb-13"></div>
      </div>

      <div style="color:#7895B2; font-size: 1.3em;">
        유통기한<br/>  
        <span style="font-size: 0.7em;">주의! : 달력에서 유통기한을 선택하지 않을 경우 유통기한 정보가 사라집니다.</span>
      </div>

      <v-date-picker
        v-model="expiry_date" 
        :landscape="true" 
        color="#7895B2"
        class=""
      >
      </v-date-picker>      

      <div class="d-flex justify-center">
         <v-checkbox label="유통기한 선택 안함" v-model="is_expiry_not_exist"></v-checkbox>
      </div>
     
      
    </v-card-text>

    <!-- 버튼 부분 -->
    <v-card-actions class="justify-center">
      <v-btn
        color="#7895B2"
        x-large
        @click="editIngre()"
      >
        수정하기
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<style>

.searchbox{
  overflow: hidden;
}

.ingredient-container{
  max-height:100px;
  overflow: scroll;
}

.units-container{
  overflow: auto;
}

.ingreName{
  display: none;
  cursor: pointer;
}

.unitsName{
  display: none;
  cursor: pointer;
}

.visible{
  display: flex;
}

</style>

<script>
import herokuAPI from '@/api/heroku.js';

export default{
  name: "editIngredient",
  data() {
    return {
      name: "",
      amount: null,
      unit: "",
      expiry_date: null,
      nickname: "",

      // 단위 목록
      units : [
        {name : "g"},
        {name : "kg"},
        {name : "l"},
        {name : "ml"},
        {name : "T"},
      ],

      // 단위 선택시를 위한 변수
      unitLabel : "단위 입력",
      
      // 유통기한 선택 안함을 위한 변수
      is_expiry_not_exist : false,
    };
  },
  props: {
    isRecipe: {
      type: Boolean,
      default: false,
    },
    idP: {
      type: Number
    },
    nameP: {
      type: String
    },
    amountP: {
      type: Number
    },
    unitP: {
      type: String
    },
  },
  mounted(){
    let vm = this;
    const UserInfo = JSON.parse(localStorage.getItem("UserInfo"));
    vm.nickname = UserInfo.nickname;

    vm.name = vm.nameP;
    vm.amount = vm.amountP;
    vm.unit = vm.unitP;

    // 동적 검색 설정
    for (var i=0;i<vm.units.length;i++){
      vm.$refs.unitsName[i].classList.remove('visible');
    }
  },
  methods: {
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
    editIngre() {
      let vm = this;
      const temp = {
        "id": vm.idP,
        "amount": Number(vm.amount),
        "expiry_date": this.is_expiry_not_exist ? null : vm.expiry_date, // 없어도 됨
        "name" : vm.name,
        "unit" : vm.unit,
      };
      if(vm.isRecipe == true) {
        vm.$emit('hide');
        vm.$emit('edit', temp);
      } else {
        const Ingre = JSON.stringify (temp);
        console.log(Ingre);
        herokuAPI.refrigeratorEdit(Ingre)
          .then(function (response) {
            console.log("response", response);
            if(response.status == 200) {
              console.log("성공 응답", response.data);
              vm.$emit('hide');
              vm.$emit('update');
            }
          })
          .catch(function (e) {
            if(e.response.status == 406) {
              console.log("406 수정실패 error");
            } else if(e.response.status == 500) {
              console.log("500 Unknown error");
            }
          });
      }
    },
    // 단위 필터
    units_filter(){
      for (var i=0;i<this.units.length;i++){
        this.$refs.unitsName[i].classList.add('visible');
      }

    },
    // 단위 클릭 시 결정
    clickUnit(payload){
      let vm = this;
      document.getElementById("inputUnit").value = " ";
      document.getElementById("inputUnit").value = payload.srcElement.innerText;
      vm.unit = payload.srcElement.innerText;
      for (var i=0;i<this.units.length;i++){
        this.$refs.unitsName[i].classList.remove('visible');
      }
      
    }
  }
}
</script>