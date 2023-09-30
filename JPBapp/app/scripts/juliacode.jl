using OffsetArrays
using Base.Threads

#-----------------------------------------------------------
# Given
#-----------------------------------------------------------
# Domain
const Ax₁, Bx₁ = 0.0, 7000.0
const Ax₂, Bx₂ = 0.0, 10500.0
const At, Bt = 0.0, 1.0

#const L₁, L₂ = 15.0, 75.0

# Mesh
const Nx₁, Nx₂ = 400, 400
const LastTimeLayer = 100000

# Media properties
# const ρ₀sf_porous = 1500.0
# const ρ₀lf_porous = 1000.0
# const cp₁_porous = 2100.0
# const cp₂_porous = 500.0
# const cs_porous = 1400.0
# const d₀_porous = 0.2


args = ARGS
# println(args)

# Media properties
const ρ₀sf_porous = parse(Float64, args[1])
const ρ₀lf_porous = parse(Float64, args[2])
const cp₁_porous = parse(Float64, args[3])
const cp₂_porous = parse(Float64, args[4])
const cs_porous = parse(Float64, args[5])
const d₀_porous = parse(Float64, args[6])

println(ρ₀sf_porous)
println(ρ₀lf_porous)
println(cp₁_porous)
println(cp₂_porous)
println(cs_porous)
println(d₀_porous)
println(args[7])


const h₁, h₂ = (Bx₁ - Ax₁) / Nx₁, (Bx₂ - Ax₂) / Nx₂
const Nt = 5*10^5
const γ = 4.0
const f₀ = 1.0
const t₀ = 1.5 
const τ = 0.00009 * h₁ / sqrt(2.0 * cp₁_porous)
const x₁₀, x₂₀ = 3500.0, 1500.0

function f(t::Float64)
    if t <= 2.0 * t₀
        exp(-(2*π* f₀ * (t-t₀))^2.0/γ^2)*sin(2.0 * π * f₀ * (t-t₀))
    else
        0.0
    end
end

#-----------------------------------------------------------
# Arrays
#-----------------------------------------------------------
const ρ₀sf = zeros(0 : Nx₂)
const ρ₀lf = zeros(0 : Nx₂)
const d₀ = zeros(0 : Nx₂)
const cp₁ = zeros(0 : Nx₂)
const cp₂ = zeros(0 : Nx₂)
const cs = zeros(0 : Nx₂)
const ρ₀s = zeros(0 : Nx₂)
const ρ₀l = zeros(0 : Nx₂)
const ρ₀ = zeros(0 : Nx₂)
const μ = zeros(0 : Nx₂)
const K = zeros(0 : Nx₂)
const α₃ = zeros(0 : Nx₂)
const α = zeros(0 : Nx₂)

const u₁ = zeros(0 : Nx₁, 0 : Nx₂)
const u₂ = zeros(0 : Nx₁, 0 : Nx₂)
const v₁ = zeros(0 : Nx₁, 0 : Nx₂-1)
const v₂ = zeros(0 : Nx₁, 0 : Nx₂-1)
const σ₁₁ = zeros(0 : Nx₁, 0 : Nx₂)
const σ₁₂ = zeros(0 : Nx₁, 0 : Nx₂)
const σ₂₂ = zeros(0 : Nx₁, 0 : Nx₂)
const p = zeros(0 : Nx₁, 0 : Nx₂)

const u₁_new = zeros(0 : Nx₁, 0 : Nx₂)
const u₂_new = zeros(0 : Nx₁, 0 : Nx₂)
const v₁_new = zeros(0 : Nx₁, 0 : Nx₂-1)
const v₂_new = zeros(0 : Nx₁, 0 : Nx₂-1)
const σ₁₁_new = zeros(0 : Nx₁, 0 : Nx₂)
const σ₁₂_new = zeros(0 : Nx₁, 0 : Nx₂)
const σ₂₂_new = zeros(0 : Nx₁, 0 : Nx₂)
const p_new = zeros(0 : Nx₁, 0 : Nx₂)

const δ = zeros(0 : Nx₁, 0 : Nx₂)
const dδ₁ = zeros(0 : Nx₁, 0 : Nx₂)
const dδ₂ = zeros(0 : Nx₁, 0 : Nx₂)

const F₁ = zeros(0 : Nx₁, 0 : Nx₂)
const F₂ = zeros(0 : Nx₁, 0 : Nx₂)

const coeff1 = zeros(0 : Nx₂)
const coeff2 = zeros(0 : Nx₂)
const coeff3 = zeros(0 : Nx₂)
const coeff4 = zeros(0 : Nx₂)


function DefineMediaCoeffs()
    porous_idx = 0 : Nx₂
    

    ρ₀sf[porous_idx] .= ρ₀sf_porous   ;
    ρ₀lf[porous_idx] .= ρ₀lf_porous   ;
    cp₁[porous_idx] .= cp₁_porous     ;
    cp₂[porous_idx] .= cp₂_porous     ;
    cs[porous_idx] .= cs_porous       ;
    d₀[porous_idx] .= d₀_porous       ;
    
    for j in 0 : Nx₂
        ρ₀s[j] = (1.0 - d₀[j]) * ρ₀sf[j]
        ρ₀l[j] = d₀[j] * ρ₀lf[j]
        ρ₀[j] = ρ₀s[j] + ρ₀l[j]
        μ[j] = ρ₀s[j] * cs[j]^2.0
    
        α₃[j] = 1.0 / (2.0 * ρ₀[j]^2.0) * (
            cp₁[j]^2.0 + cp₂[j]^2.0 -
            8.0 / 3.0 * ρ₀s[j] * cs[j]^2.0 / ρ₀[j] +
            sqrt(
                (cp₁[j]^2.0 - cp₂[j]^2.0)^2.0 -
                64.0 / 9.0 * ρ₀l[j] * ρ₀s[j] * cs[j]^4.0 / ρ₀[j]^2.0
            )
        )
    end
    
    for j in porous_idx
        K[j] = 0.5 * ρ₀[j] * ρ₀s[j] / ρ₀l[j] * (
            cp₁[j]^2.0 + cp₂[j]^2.0 -
            8.0 / 3.0 * ρ₀l[j] * cs[j]^2.0 / ρ₀[j] -
            sqrt(
                (cp₁[j]^2.0 - cp₂[j]^2.0)^2.0 -
                64.0 / 9.0 * ρ₀l[j] * ρ₀s[j] * cs[j]^4.0 / ρ₀[j]^2.0
            )
        )
        α[j] = ρ₀[j] * α₃[j] + K[j] / ρ₀[j]^2.0
    end
end


function DefineCoeffs()
    for j in 0 : Nx₂
        
        coeff1[j] = (ρ₀s[j] * K[j] / ρ₀[j] - 2.0 * μ[j] / 3.0)
        coeff2[j] = ρ₀s[j] * K[j] / ρ₀[j]
        coeff3[j] = -(K[j] - α[j] * ρ₀[j] * ρ₀s[j])
        coeff4[j] = α[j] * ρ₀[j] * ρ₀l[j]
       
    end
end


function DefineDelta()
    a = 2.0 * max(h₁, h₂)
    a² = a^2.0

    for i in 0 : Nx₁, j in 0 : Nx₂
        x₁ = Ax₁ + i * h₁
        x₂ = Ax₂ + j * h₂
        R² = (x₁ - x₁₀)^2.0 + (x₂ - x₂₀)^2.0

        if R² < a²
            δ[i,j] = exp(-a² / (a² - R²))
            dδ₁[i,j] = -2.0 * a² * (x₁ - x₁₀) * exp(-a² / (a² - R²)) / (a² - R²)^2.0
            dδ₂[i,j] = -2.0 * a² * (x₂ - x₂₀) * exp(-a² / (a² - R²)) / (a² - R²)^2.0
        end
    end
end


function DefineRHS(n::Int64)
    @inbounds @threads for i in 0 : Nx₁-1
        @inbounds for j in 0 : Nx₂-1
            f_mid = 0.5 * (f(τ * n) + f(τ * (n + 1)))
            F₁[i,j] = 0.5 * f_mid * (dδ₁[i,j] * δ[i,j] + dδ₁[i+1,j] * δ[i+1,j])
            F₂[i,j] = 0.5 * f_mid * (δ[i,j] * dδ₂[i,j] + δ[i,j+1] * dδ₂[i,j+1])
        end
    end
end


function Integrate()
    @inbounds @threads for j in Nx₂-1 : -1 : 1
        @inbounds for i in Nx₁-1 : -1 : 1
            u₁_new[i,j] = u₁[i,j] - τ * (
                (σ₁₁[i+1,j] - σ₁₁[i,j]) / (h₁ * ρ₀s[j]) +
                (σ₁₂[i,j+1] - σ₁₂[i,j]) / (h₂ * ρ₀s[j]) +
                (p[i+1,j] - p[i,j]) / (h₁ * ρ₀[j]) -
                F₁[i,j]
            )
        end
    end
    
    @inbounds @threads for i in Nx₁-1 : -1 : 1
        @inbounds for j in Nx₂-1 : -1 : 1
            u₂_new[i,j] = u₂[i,j] - τ * (
                (σ₁₂[i+1,j] - σ₁₂[i,j]) / (h₁ * ρ₀s[j]) +
                (σ₂₂[i,j+1] - σ₂₂[i,j]) / (h₂ * ρ₀s[j]) +
                (p[i,j+1] - p[i,j]) / (h₂ * ρ₀[j]) -
                F₂[i,j]
            )
        end
    end
    
    @inbounds @threads for j in 0 : Nx₂-1
        @inbounds for i in 0 : Nx₁-1
            v₁_new[i,j] = v₁[i,j] - τ * (
                (p[i+1,j] - p[i,j]) / (ρ₀[j] * h₁) -
                F₁[i,j]
            )
        end
    end
    
    @inbounds @threads for i in Nx₁-1 : -1 : 1
        @inbounds for j in Nx₂-1 : -1 : 1
            v₂_new[i,j] = v₂[i,j] - τ * (
                (p[i,j+1] - p[i,j]) / (ρ₀[j] * h₂) -
                F₂[i,j]
            )
        end
    end
    
    @inbounds @threads for j in 1 : Nx₂-1
        @inbounds for i in 1 : Nx₁-1
            σ₁₁_new[i,j] = σ₁₁[i,j] - τ * (
                2.0 * μ[j] * (u₁[i,j] - u₁[i-1,j]) / h₁ +
                coeff1[j] * ( 
                    (u₁[i,j] - u₁[i-1,j]) / h₁ +
                    (u₂[i,j] - u₂[i,j-1]) / h₂
                ) -
                coeff2[j] * (
                    (v₁[i,j] - v₁[i-1,j]) / h₁ +
                    (v₂[i,j] - v₂[i,j-1]) / h₂
                )
            )
        end
    end
    
    @inbounds @threads for j in 1 : Nx₂-1
        @inbounds for i in 1 : Nx₁-1
            σ₁₂_new[i,j] = σ₁₂[i,j] - τ * μ[j] * (
                (u₁[i,j] - u₁[i,j-1]) / h₂ +
                (u₂[i,j] - u₂[i-1,j]) / h₁
            )
        end
    end
    
    
    @inbounds @threads for j in 1 : Nx₂-1
        @inbounds for i in 1 : Nx₁-1
            σ₂₂_new[i,j] = σ₂₂[i,j] - τ * (
                2.0 * μ[j] * (u₂[i,j] - u₂[i,j-1]) / h₂ +
                coeff1[j] * (
                    (u₁[i,j] - u₁[i-1,j]) / h₁ +
                    (u₂[i,j] - u₂[i,j-1]) / h₂
                ) -
                coeff2[j] * (
                    (v₁[i,j] - v₁[i-1,j]) / h₁ +
                    (v₂[i,j] - v₂[i,j-1]) / h₂
                )
            )
        end
    end
    
    @inbounds @threads for j in 1 : Nx₂-1
        @inbounds for i in 1 : Nx₁-1
            p_new[i,j] = p[i,j] - τ * (
                coeff3[j] * (
                    (u₁[i,j] - u₁[i-1,j]) / h₁ +
                    (u₂[i,j] - u₂[i,j-1]) / h₂
                ) +
                coeff4[j] * (
                    (v₁[i,j] - v₁[i-1,j]) / h₁ +
                    (v₂[i,j] - v₂[i,j-1]) / h₂
                )
            )
        end
    end
end


function DumpParaview(n::Int64)
    @assert any(isnan, u₁) == false

    io = open("data/data.$(n).csv", "w")
    println(io, "x1,x2,u,v,sigma11,sigma12,sigma22,p")
    @inbounds for i in 0 : Nx₁
        @inbounds for j in 0 : Nx₂
            u, v = 0.0, 0.0
            if 1 <= i <= Nx₁-1 && 1 <= j <= Nx₂-1
                u = 0.5 * sqrt(
                    (u₁[i-1,j] + u₁[i,j])^2.0 + 
                    (u₂[i-1,j] + u₂[i,j])^2.0
                )
                v = 0.5 * sqrt(
                    (v₁[i,j-1] + v₁[i,j])^2.0 + 
                    (v₂[i,j-1] + v₂[i,j])^2.0
                )
            end
        
            println(io, "$(Ax₁+i*h₁),$(Ax₂+j*h₂),$(u),$(v),$(σ₁₁[i,j]),$(σ₁₂[i,j]),$(σ₂₂[i,j]),$(p[i,j])")
        end
    end
    close(io)
end


function UpdateTimeLayers()
    u₁ .= u₁_new
    u₂ .= u₂_new
    v₁ .= v₁_new
    v₂ .= v₂_new
    σ₁₁ .= σ₁₁_new
    σ₁₂ .= σ₁₂_new
    σ₂₂ .= σ₂₂_new
    p .= p_new
end


function Start()
    DefineDelta()
    DefineMediaCoeffs()
    DefineCoeffs()

    for n in 0 : LastTimeLayer-1
        if n%10000 == 0
            println(n)
        end
        if n % 1000 == 0 
            DumpParaview(n)
        end
        DefineRHS(n)
        Integrate()
        UpdateTimeLayers()
    end
    
    DumpParaview(LastTimeLayer)
end
print(τ)

# Start()
