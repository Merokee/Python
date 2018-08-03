#!/bin/bash

echo "first_step脚本名称：$0"
:<<!
echo "second_step"
!
echo "third_step脚本传入参数：$1"
echo "third_step脚本传入参数：$2"
echo "third_step脚本传入参数：$3"
echo "third_step脚本传入参数：$4"
# $# 表示传入参数的个数
echo "脚本传入参数个数$#"
