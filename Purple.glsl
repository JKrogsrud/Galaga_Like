void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = fragCoord / iResolution.xy;

    vec2 rpos = uv - 0.5;
    // Adjust y by aspect ratio
    rpos.y /= iResolution.x / iResolution.y;

    float distance = length(rpos);

    float scale = 0.1;
    float strength = 1.0 / distance * scale;

    vec3 color = strength * vec3(0.5, 0.0, 0.7);

    fragColor = vec4(color, 1.0);
}