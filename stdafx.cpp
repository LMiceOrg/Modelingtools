#include "stdafx.h"
/** FIXED [TODO] 增加错误提示功能 */
/** FIXED [TODO]:Python embed helper class */

/** NOTE: 在C++与Python之间传递参数使用UTF-8编码格式 */
/** FIXED: 增加工程文档描述和管理 */
/** FIXED: Excel文件最后的空行会造成解析错误！！*/
/** FIXED: EmbedPython: UnicodeEncodeError cannot process */
/** NOTE:  性能参数多粒度的用逗号分隔（列）结尾用分号分隔（行）
11,12,13;
21,22,23;
31,32,33;
11,12,13;21,22,23;31,32,33;
*/

/** NOTE: 复合数据结构中的多粒度参数解析 在列（粒度）的值为(1+), 其粒度数量是上一个字段 */

/** NOTE: 不同命名空间中的类型有相互引用的关系，解决方案：对引用的其他命名空间的类型做声明前置

//来自通讯类的类型声明
 struct aaa;

// 平台类定义
 struct plat_bbb {
     aaa a;
 };

*/

/** NOTE: 单元测试框架的技术方案 Python Extention
 * 方案2: Luajit + ToLua++
*/

/** FIXED: what are xsi:types of user defined types
 * builder/xmlmodeldescbuilder  CreateModelInitParamItem
 */


/** FIXED: Excel G4 文件名有错误 */

/**
 * https://msdn.microsoft.com/en-us/library/windows/desktop/aa365247(v=vs.85).aspx
 * Naming Files, Paths, and Namespaces
 *
 *  FIXED: 设备型号 判断非法字符，生成ini文件 (ini builder )
 *
 *  FIXED: 性能参数文件名根据 设备名称 ＋.ini (无效字符替换) (impl cpp)
 *
 *  FIXED: 超低空飞行时间 600，超高速飞行时间 600 在datadefine中定义基准时间
 *
 *
*/
