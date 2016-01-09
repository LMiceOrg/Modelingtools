#include "stdafx.h"

/** NOTE: 在C++与Python之间传递参数使用UTF-8编码格式 */
/** FIXME: 增加工程文档描述和管理 */
/** FIXME: Excel文件最后的空行会造成解析错误！！*/
/** FIXME: EmbedPython: UnicodeEncodeError cannot process */
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


