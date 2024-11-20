



export function getCategories(): Promise<any>{
    return fetch('/api/courses/categories')
}